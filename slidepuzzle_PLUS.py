# SlidePuzzlePlus
# By Greg Schaefer (schae029@gmail.com) and Al Sweigart (al@inventwithpython.com)
# Released under a GNU GPLv3 license.

#  Copyright (C) 2020 by Gregory N. Schaefer
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  (License is found in the COPYING.txt file.)
#    If not, see <https://www.gnu.org/licenses/>.

##############################################################################
### Acknowledgments:
##############################################################################

# SlidePuzzlePlus is an enhancement of Al Sweigart's "Slide Puzzle" game which
# is released under a "Simplified BSD" License.  
# See http://inventwithpython.com/pygame and Chapter 4 (Slide Puzzle) of
# Sweigart's book, "Making Games with Python and Pygame" (2012).

# Sweigart's Slide Puzzle functions are all found in this source code file,
# slidepuzzle_PLUS.py, with the exception of 'getPosition', which is found in
# my constants_and_genFtns.py file.  
# Sweigart's functions include the following:

#   - main (with modifications by Greg Schaefer)
#   - terminate
#   - checkForQuit
#   - getStartingBoard
#   - getBlankPosition
#   - makeMove (with modifications by Greg Schaefer)
#   - getPosition (found in constants_and_genFtns.py)
#   - isValidMove
#   - getRandomMove
#   - getLeftTopOfTile
#   - getSpotClicked
#   - drawTile
#   - makeText
#   - drawBoard
#   - slideAnimation (with modifications by Greg Schaefer)
#   - generateNewPuzzle
#   - resetAnimation 


# In this file, functions written by Greg Schaefer include:

#   - updateClickCountSurf
#   - updateTimeSurf
#   - getGameScore

# slidepuzzle_PLUS imports the following modules, all authored by Greg Schaefer:

#   - constants_and_genFtns.py
#   - makeAdjacent4.py
#   - order4.py
#   - getTiles.py
#   - slidePuzzle_algorithm.py

##############################################################################
###
##############################################################################

import pygame, sys, random, os
from constants_and_genFtns import *
from makeAdjacent4 import *
from order4 import *
from getTiles import *
from slidePuzzle_algorithm import *
from pygame.locals import *
from datetime import datetime


TILESIZE = 80
# WINDOWWIDTH = 640  # original size
WINDOWWIDTH = 700
# WINDOWHEIGHT = 480  # original size
WINDOWHEIGHT = 525
FPS = 40
TIMEPERGAME = 160  # time is in seconds (default will be 130 seconds)

#                 R    G    B
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
GREEN =         (  0, 204,   0)

BGCOLOR = DARKTURQUOISE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20
SMALLFONTSIZE = 18

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

LEFT_OFFSET = 70
XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2) + 40
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF
    global NEW_RECT, SMALLFONT, ALG_SURF, ALG_RECT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Slide Puzzle +')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    SMALLFONT = pygame.font.SysFont('timesnewroman', SMALLFONTSIZE)

    # Store the option buttons and their rectangles.
    RESET_SURF, RESET_RECT = makeText('Reset',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 70)
    NEW_SURF,   NEW_RECT   = makeText('New Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 40)

    # Create button for the computer to play.
    ALG_SURF, ALG_RECT = makeText('Compute Move', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 300, WINDOWHEIGHT - 70)

    mainBoard, solutionSeq = generateNewPuzzle(130)
    # A solved board is the same as the board in a start state, prior to any
    # scrambling of the tiles (which is done in generateNewPuzzle).
    SOLVEDBOARD = getStartingBoard()
    allMoves = []  # list of moves made from the solved configuration
    clicks = 0  # Keep track of the number of moves made

    # start countdown clock
    clock_start = datetime.now()
    time_flag = 'OFF'   # needed to delay start of countdown clock
    timedOutFlag = False  # if True, player has used up all of their time
    prev_time = None
    time_remaining = TIMEPERGAME  # initialize time_remaining
    calcFinalScore = True  # want to calculate final score only once after the puzzle is solved
    showClock = True
    alg_ON = False
    lastMove = None

    while True:  # main game loop
        slideTo = None  # the direction, if any, a tile should slide
        msg = 'Click tile or press arrow keys to slide.'  # msg for upper left corner.
        if mainBoard == SOLVEDBOARD:
            msg = SOLVED
            if calcFinalScore:
                FinalScoreTextSurf, FinalScoreTextRect = getGameScore(clicks, time_remaining,
                                                                      timedOutFlag, alg_ON)
                calcFinalScore = False

        drawBoard(mainBoard, msg)
        updateClickCountSurf(clicks)  # blits the tile move count to the screen
        # updateTimeSurf also blits to the screen
        clock_start, time_remaining, time_flag, prev_time = updateTimeSurf(time_flag, clock_start,
                                                                           prev_time, msg, timedOutFlag)

        if time_remaining <= 0 and not alg_ON:
            msg = 'Your time is up!  Try again?'
            timedOutFlag = True
            drawBoard(mainBoard, msg)
            updateClickCountSurf(clicks)  # blits the tile move count to the screen
            if calcFinalScore:
                FinalScoreTextSurf, FinalScoreTextRect = getGameScore(clicks, time_remaining,
                                                                      timedOutFlag, alg_ON)
                calcFinalScore = False
        # the Final Score line is displayed only if we timed out or if the
        # puzzle was solved.
        if msg == SOLVED or timedOutFlag:
            DISPLAYSURF.blit(FinalScoreTextSurf, FinalScoreTextRect)

        checkForQuit()
        for event in pygame.event.get():  # event handling loop
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])

                if (spotx, spoty) == (None, None):
                    # check if the user clicked on an option button
                    if RESET_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, allMoves, alg_ON)  # clicked on Reset button
                        allMoves = []
                        clicks = 0
                        clock_start = datetime.now()
                        time_flag = 'OFF'
                        timedOutFlag = False
                        calcFinalScore = True
                        alg_ON = False
                        lastMove = None
                    elif NEW_RECT.collidepoint(event.pos):
                        mainBoard, solutionSeq = generateNewPuzzle(130)  # clicked on New Game button
                        allMoves = []
                        clicks = 0
                        clock_start = datetime.now()
                        time_flag = 'OFF'
                        timedOutFlag = False
                        calcFinalScore = True
                        alg_ON = False
                        lastMove = None
                    elif ALG_RECT.collidepoint(event.pos):  # clicked on Compute Move button
                        # run computer algorithm one move at a time; send it
                        # the previous move so that we do not repeat it
                        alg_ON = True
                        slideTo = getNextMove(mainBoard, lastMove, SOLVEDBOARD)
                elif not timedOutFlag and msg != SOLVED and not alg_ON:
                    # check if the clicked tile was next to the blank spot
                    blankx, blanky = getBlankPosition(mainBoard)
                    if spotx == blankx + 1 and spoty == blanky:
                        slideTo = LEFT
                    elif spotx == blankx - 1 and spoty == blanky:
                        slideTo = RIGHT
                    elif spotx == blankx and spoty == blanky + 1:
                        slideTo = UP
                    elif spotx == blankx and spoty == blanky - 1:
                        slideTo = DOWN

        # When the computer is not making a move, slideTo has a value only
        # if player has neither timed out nor solved the puzzle.
        if slideTo and slideTo != 'Stop':
            lastMove = slideTo
            animationSpeed = 8
            slideAnimation(mainBoard,
                           slideTo, 'Click tile or press arrow keys to slide.',
                           animationSpeed, alg_ON)  # show slide on screen
            makeMove(mainBoard, slideTo, alg_ON)
            allMoves.append(slideTo) # record the slide
            clicks += 1

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT):  # get all the QUIT events
        terminate()  # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP):  # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate()  # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event)  # put the other KEYUP event objects back


def getStartingBoard():
    # Return a board data structure with tiles in the solved state.
    # For example, if BOARDWIDTH and BOARDHEIGHT are both 3, this function
    # returns [[1, 4, 7], [2, 5, 8], [3, 6, BLANK]]
    counter = 1
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(counter)
            counter += BOARDWIDTH
        board.append(column)
        counter -= BOARDWIDTH * (BOARDHEIGHT - 1) + BOARDWIDTH - 1

    board[BOARDWIDTH-1][BOARDHEIGHT-1] = BLANK
    return board


def getBlankPosition(board):
    # Return the x and y of board coordinates of the blank space.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == BLANK:
                return (x, y)


def makeMove(board, move, alg_ON=False):
    # This function does not check if the move is valid.
    blankx, blanky = getBlankPosition(board)

    # gns: the tile the player clicks on is what is moving up, down, left, or right
    if not alg_ON:
        if move == UP:
            board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
        elif move == DOWN:
            board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
        elif move == LEFT:
            board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
        elif move == RIGHT:
            board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]
    # gns: when the algorithm controls the game, it is the blank tile that
    # moves UP, DOWN, LEFT, or RIGHT.        
    elif alg_ON:
        if move == UP:
            board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
        elif move == DOWN:
            board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
        elif move == LEFT:
            board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]
        elif move == RIGHT:
            board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]


def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != len(board) - 1) or \
           (move == RIGHT and blankx != 0)


def getRandomMove(board, lastMove=None):
    # start with a full list of all four moves
    validMoves = [UP, DOWN, LEFT, RIGHT]

    # remove moves from the list as they are disqualified
    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP)
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)

    # return a random move from the list of remaining moves
    return random.choice(validMoves)


def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1) + LEFT_OFFSET
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)


def getSpotClicked(board, x, y):
    # from the x & y pixel coordinates, get the x & y board coordinates
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)


def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    # draw a tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and adjy)
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)


def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def updateClickCountSurf(clicks):
    text = 'Tiles Clicked: ' + str(clicks)
    textSurf = SMALLFONT.render(text, True, TEXTCOLOR, BGCOLOR)
    textRect = textSurf.get_rect()
    left, top = getLeftTopOfTile(0, 0)
    textRect.topleft = (left - (210 + LEFT_OFFSET), top - 20)
    DISPLAYSURF.blit(textSurf, textRect)


def updateTimeSurf(time_flag, start, prev_tdelta, msg, timedOutFlag):
    if time_flag == 'ON':
        stop = datetime.now()
        tdelta = stop - start
    else:
        start = datetime.now()
        tdelta = start - start
        time_flag = 'ON'

    if (msg == SOLVED) or timedOutFlag:
        prev_tdelta = prev_tdelta
    else:
        prev_tdelta = tdelta

    time_remaining = TIMEPERGAME - prev_tdelta.seconds
    text = 'Time remaining: ' + str(time_remaining) + ' secs'
    textSurf = SMALLFONT.render(text, True, TEXTCOLOR, BGCOLOR)
    textRect = textSurf.get_rect()
    left, top = getLeftTopOfTile(0, 0)
    textRect.topleft = (left - (210 + LEFT_OFFSET), top - 50)
    DISPLAYSURF.blit(textSurf, textRect)
    return start, time_remaining, time_flag, prev_tdelta


def getGameScore(clicks, time_remaining, timedOutFlag, alg_ON):
    if not alg_ON:
        final_score = (TIMEPERGAME - time_remaining) + clicks
        if timedOutFlag:
            final_score += TIMEPERGAME
        # When SOLVE button existed, players could cheat by clicking a few tiles
        # and then hitting the SOLVE button.  If player times out but hardly
        # clicks, they get a heavy penalty.
        if timedOutFlag and clicks < 40:
            final_score = 3 * (TIMEPERGAME + 50)
    elif alg_ON:
        final_score = clicks
    text = 'FINAL SCORE: ' + str(final_score)
    textSurf = SMALLFONT.render(text, True, TEXTCOLOR, BGCOLOR)
    textRect = textSurf.get_rect()
    left, top = getLeftTopOfTile(0, 0)
    textRect.topleft = (left - (210 + LEFT_OFFSET), top + 15)
    return textSurf, textRect


def drawBoard(board, message):
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)

    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])

    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(ALG_SURF, ALG_RECT)


def slideAnimation(board, direction, message, animationSpeed, alg_ON=False):
    # This function does not check if the move is valid.
    blankx, blanky = getBlankPosition(board)
    if not alg_ON:
        if direction == UP:
            movex = blankx
            movey = blanky + 1
        elif direction == DOWN:
            movex = blankx
            movey = blanky - 1
        elif direction == LEFT:
            movex = blankx + 1
            movey = blanky
        elif direction == RIGHT:
            movex = blankx - 1
            movey = blanky
    elif alg_ON:
        if direction == UP:
            movex = blankx
            movey = blanky - 1
        elif direction == DOWN:
            movex = blankx
            movey = blanky + 1
        elif direction == LEFT:
            movex = blankx - 1
            movey = blanky
        elif direction == RIGHT:
            movex = blankx + 1
            movey = blanky

    # prepare the base surface
    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()
    # draw a blank space over the moving tile on the baseSurf Surface.
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

    for i in range(0, TILESIZE, animationSpeed):
        # animate the tile sliding over
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if not alg_ON:
            if direction == UP:
                drawTile(movex, movey, board[movex][movey], 0, -i)
            if direction == DOWN:
                drawTile(movex, movey, board[movex][movey], 0, i)
            if direction == LEFT:
                drawTile(movex, movey, board[movex][movey], -i, 0)
            if direction == RIGHT:
                drawTile(movex, movey, board[movex][movey], i, 0)
        elif alg_ON:
            if direction == UP:
                drawTile(movex, movey, board[movex][movey], 0, i)
            if direction == DOWN:
                drawTile(movex, movey, board[movex][movey], 0, -i)
            if direction == LEFT:
                drawTile(movex, movey, board[movex][movey], i, 0)
            if direction == RIGHT:
                drawTile(movex, movey, board[movex][movey], -i, 0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generateNewPuzzle(numSlides):
    # From a starting configuration, make numSlides number of moves (and
    # animate these moves).
    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')  # 2nd argument is for msg
    pygame.display.update()
    pygame.time.wait(500) # pause 500 milliseconds for effect
    lastMove = None
    for i in range(numSlides):
        move = getRandomMove(board, lastMove)
        slideAnimation(board, move, 'Generating new puzzle . . .',
                       animationSpeed=int(TILESIZE / 3))
        makeMove(board, move)
        sequence.append(move)
        lastMove = move
    return (board, sequence)


def resetAnimation(board, allMoves, alg_ON=False):
    # make all of the moves in allMoves in reverse.
    revAllMoves = allMoves[:] # gets a copy of the list
    revAllMoves.reverse()

    for move in revAllMoves:
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == RIGHT:
            oppositeMove = LEFT
        elif move == LEFT:
            oppositeMove = RIGHT
        animationSpeed = int(TILESIZE / 2)
        slideAnimation(board, oppositeMove, '', animationSpeed, alg_ON)
        makeMove(board, oppositeMove, alg_ON)


if __name__ == '__main__':
    main()

##############################################################################
###
##############################################################################








