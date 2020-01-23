
#############################################################################
### spPLUS_TESTING_module.py COPYRIGHT:
#############################################################################

# SlidePuzzlePlus, spPLUS_TESTING_module.py
# By Greg Schaefer (gnsphd@outlook.com)

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
 
# Sweigart's Slide Puzzle functions used in this test module include
# the following:

#   - main (with MAJOR modifications by Greg Schaefer)
#   - getStartingBoard
#   - getBlankPosition
#   - makeMove (with modifications by Greg Schaefer)
#   - getPosition (found in constants_and_genFtns.py)
#   - isValidMove
#   - getRandomMove
#   - generateNewPuzzle  

##############################################################################
### spPLUS_TESTING_module.py
##############################################################################

import pdb
import json
import sys, random, os
from constants_and_genFtns import *
from makeAdjacent4 import *
from order4 import *
from getTiles import *
from slidePuzzle_algorithm import *
from datetime import datetime


def main():
    
    filepath = '  '
    filename = 'sp_testResults.json'
    myfile = filepath + filename
    datafile = filepath + 'sp_allTestResults.json'

    mainBoard, solutionSeq = generateNewPuzzle(140)
    # A solved board is the same as the board in a start state, prior to any
    # scrambling of the tiles (which is done in generateNewPuzzle).
    SOLVEDBOARD = getStartingBoard()
    
    newBoard = str(mainBoard[:])
    allMoves = []  # list of moves made from the solved configuration
    clicks = 0  # Keep track of the number of moves made
    lastMove = None

    boardsToTest = 100000
    n = 0
    problem = False
    # testResults = []
    testBoards = []
    results = []
    
    # testBoards.append(newBoard)

    while n < boardsToTest and problem == False:  # OUTER LOOP
        if n > 0:
            mainBoard, solutionSeq = generateNewPuzzle(140)   # New Game
            newBoard = str(mainBoard[:])
            # testBoards.append(newBoard)
            allMoves = []
            clicks = 0
            lastMove = None
            
        msg = 'Click tile or press arrow keys to slide.'

        while msg != SOLVED and problem == False:  # INNER LOOP
            slideTo = None
            alg_ON = True
            if mainBoard == SOLVEDBOARD:
                msg = SOLVED
                # testResults.append({newBoard: clicks})
                results.append(clicks)
                        
            if msg != SOLVED:
                slideTo = getNextMove(mainBoard, lastMove, SOLVEDBOARD)

            if slideTo:
                lastMove = slideTo
                makeMove(mainBoard, slideTo, alg_ON)
                allMoves.append(slideTo)
                clicks += 1
                # the code is broken if we go over 350 moves.
            if clicks > 350 or (slideTo is None and msg != SOLVED):
                problem = True
                # testResults.append({newBoard: clicks})
                results.append(clicks)
            ### END OF INNER WHILE  LOOP
        n += 1
        ### END OF OUTER WHILE LOOP
    if problem == True:
        testBoards.append(newBoard)
    with open(myfile, 'w') as file_object:
        json.dump(testBoards, file_object)
    with open(datafile, 'a') as file2:
        json.dump(results, file2)
    # print(results)
    print("The length of testResults is: ", len(results))


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

    if not alg_ON:
        if move == UP:
            board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
        elif move == DOWN:
            board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
        elif move == LEFT:
            board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
        elif move == RIGHT:
            board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]
    # When the algorithm controls the game, it is the blank tile that moves
    # UP, DOWN, LEFT, or RIGHT.        
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


def generateNewPuzzle(numSlides):
    # From a starting configuration, make numSlides number of moves (and
    # animate these moves).
    sequence = []
    board = getStartingBoard()
    lastMove = None
    for i in range(numSlides):
        move = getRandomMove(board, lastMove)
        makeMove(board, move)
        sequence.append(move)
        lastMove = move
    return (board, sequence)


start = datetime.now()
if __name__ == '__main__':
    main()
stop = datetime.now()
delta = stop - start
time_val = round(delta.seconds + delta.microseconds/1000000, 2)
print(time_val)

# test pgm needs 15 - 18 minutes to run 100,000 boards through the algorithm.

filepath = '  '
datafile = filepath + 'sp_allTestResults.json'
with open(datafile) as f_obj:
    mydat = json.load(f_obj)

print("Number of trials is: ", str(len(mydat)))
print("Maximum number of clicks is: ", str(max(mydat)))
print("Minimum number of clicks is: ", str(min(mydat)))


import numpy as np
print(np.mean(mydat))
print(np.median(mydat))



##############################################################################
###
##############################################################################





##############################################################################
###
##############################################################################








