# -*- coding: utf-8 -*-
"""
@author: Greg Schaefer

program name: slidePuzzle_algorithm.py

module contents (11 ftns):
    
    - getNextMove
    - adjacent4
    - blankCW
    - blankCW02
    - blankCW03
    - moveClockwise
    - readyToRotate
    - finalRsReady
    - orderLast3Ts
    - putLast3betw
    - moveLast3Ts
    - continueDir
    
Released under a GNU GPLv3 license. 

"""

#############################################################################
### slidePuzzle_algorithm.py COPYRIGHT:
#############################################################################

# SlidePuzzlePlus, slidePuzzle_algorithm.py
# By Greg Schaefer (schae029@gmail.com)

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
# Algorithm to solve the 4-by-4 slide puzzle.
##############################################################################

from makeAdjacent4 import *
from order4 import *
from getTiles import *
from constants_and_genFtns import *

##############################################################################
# main algorithm
##############################################################################

# This ftn contains the logic for determining the next "best" move of the blank.
# 'board' is a 4-element list, each element of which is itself a 4-element list.
# Each element of board is a column of the numbers on the game board.
# The value of board[x][y] will be one of 1 - 15 or BLANK (= None).
# Note that x picks out the column of the board we want to work with, and
# y picks out the row in that column that we want to work with.
def getNextMove(board, lastMove, SOLVEDBOARD):
    """ Computes the next "best" move for the blank on the given board.  Return
    value is one of UP, DOWN, RIGHT, LEFT."""
    
    blankx, blanky = getPosition(board, BLANK)

    # First check to see whether the first Row is completed.
    firstRowDone = (board[0][0] == 1 and board[1][0] == 2 and board[2][0] == 3
                    and board[3][0] == 4 and blanky in (1, 2, 3))
    secondRowDone = (board[0][1] == 5 and board[1][1] == 6 and
                     board[2][1] == 7 and board[3][1] == 8 and blanky in (2, 3))
    # if firstRow is not done, see if it is ready:
    if not firstRowDone:
        # get locations of 1, 2, 3, and 4
        T1x, T1y = getPosition(board, 1)
        T2x, T2y = getPosition(board, 2)
        T3x, T3y = getPosition(board, 3)
        T4x, T4y = getPosition(board, 4)
        topRow, bottomRow = 0, 1

        # General idea for the algorithm: address the most finished states first.

        allTsInPlace1stRow = (blanky <= 1 and T1y <= 1 and T2y <= 1 and
                              T3y <= 1 and T4y <= 1)

        # If 1-4 and blank are in top two rows, and if we have the correct
        # order among the tiles, then we are almost done with the first row.
        # After establishing contiguity, we only need to rotate the firstRow
        # tiles into their final positions.
        if allTsInPlace1stRow:
            # see whether the tiles are correctly ordered:
            firstRowReady = readyToRotate(T1x, T1y, T2x, T2y, T3x, T3y, T4x, T4y,
                                          blankx, blanky, topRow, bottomRow)
            if firstRowReady:
                # need tiles 1-4 to be separated only by the blank before we
                # can rotate
                allAdjacent = adjacent4(T1x, T1y, T2x, T2y, T3x, T3y, T4x, T4y,
                                        blankx, blanky)
                if allAdjacent:
                    # establish whether we move blank CW or counter-CW
                    if blankCW(T1x, T1y, T2x, T2y, T3x, T3y, T4x, T4y, blankx,
                               blanky):
                        nextMove = moveClockwise(blankx, blanky, topRow, bottomRow)
                        return nextMove
                    else:
                        nextMove = continueDirCCW(blankx, blanky, topRow, bottomRow)
                        return nextMove
                elif not allAdjacent:
                    nextMove = makeAdjacent4(T1x, T1y, T2x, T2y, T3x, T3y, T4x,
                                             T4y, blankx, blanky)
                    # ensure we don't get caught in an infinite loop:
                    if nextMove == oppDirection(lastMove):
                        nextMove = continueDir(lastMove, blankx, blanky,
                                               topRow, bottomRow)
                    return nextMove
            elif not firstRowReady:
                # We have all of the tiles in the correct rows but they are
                # out of order.
                nextMove = order4('first', board)
                # ensure we don't get caught in an infinite loop:
                if nextMove == oppDirection(lastMove):
                    nextMove = continueDir(lastMove, blankx, blanky, topRow,
                                           bottomRow)
                return nextMove
        elif not allTsInPlace1stRow:
            nextMove = getTiles('first', board, lastMove)
            # ensure we don't get caught in an infinite loop:
            if nextMove == oppDirection(lastMove):
                nextMove = continueDir(lastMove, blankx, blanky, topRow, bottomRow)
            return nextMove
    elif not secondRowDone:
        # get locations of 5, 6, 7, and 8
        T5x, T5y = getPosition(board, 5)
        T6x, T6y = getPosition(board, 6)
        T7x, T7y = getPosition(board, 7)
        T8x, T8y = getPosition(board, 8)
        topRow, bottomRow = 1, 2

        allTsInPlace2ndRow = (blanky in (1, 2) and T5y in (1, 2) and
                              T6y in (1, 2) and T7y in (1, 2) and
                              T8y in (1, 2))

        if allTsInPlace2ndRow:
            # If 5-8 and blank are in the second and third rows, and if the
            # tiles are in the correct order, then we are almost done with
            # the second row; after establishing contiguity, we can rotate the
            # secondRow tiles into their final positions.
            # See whether the tiles are correctly ordered:
            secondRowReady = readyToRotate(T5x, T5y, T6x, T6y, T7x, T7y, T8x, T8y,
                                           blankx, blanky, topRow, bottomRow)
            if secondRowReady:
                # need tiles 5-8 to be separated only by the blank before we
                # can rotate
                allAdjacent = adjacent4(T5x, T5y, T6x, T6y, T7x, T7y, T8x, T8y,
                                        blankx, blanky)
                if allAdjacent:
                    # establish whether we move blank CW or counter-CW
                    if blankCW(T5x, T5y, T6x, T6y, T7x, T7y, T8x, T8y, blankx,
                               blanky):
                        nextMove = moveClockwise(blankx, blanky, topRow, bottomRow)
                        return nextMove
                    else:
                        nextMove = continueDirCCW(blankx, blanky, topRow, bottomRow)
                        return nextMove
                elif not allAdjacent:
                    nextMove = makeAdjacent4(T5x, T5y, T6x, T6y, T7x, T7y, T8x,
                                             T8y, blankx, blanky)
                    # ensure we don't get caught in an infinite loop:
                    if nextMove == oppDirection(lastMove):
                        nextMove = continueDir(lastMove, blankx, blanky,
                                               topRow, bottomRow)
                    return nextMove
            elif not secondRowReady:
                # All of the tiles are in the correct rows but they are out of
                # order.
                nextMove = order4('second', board)
                # ensure we don't get caught in an infinite loop:
                if nextMove == oppDirection(lastMove):
                    nextMove = continueDir(lastMove, blankx, blanky, topRow,
                                           bottomRow)
                return nextMove
        elif not allTsInPlace2ndRow:
            nextMove = getTiles('second', board, lastMove)
            # ensure we don't get caught in an infinite loop:
            if nextMove == oppDirection(lastMove):
                nextMove = continueDir(lastMove, blankx, blanky, topRow, bottomRow)
            return nextMove
    else:
        # The final two rows remain unfinished.
        # final steps: order the tiles; then move them into place.
        # blank is in either row 2 or row 3
        # get locations of 9-12, 13-15, and blank tile
        blankx, blanky = getPosition(board, BLANK)
        T9x, T9y = getPosition(board, 9)
        T10x, T10y = getPosition(board, 10)
        T11x, T11y = getPosition(board, 11)
        T12x, T12y = getPosition(board, 12)
        T13x, T13y = getPosition(board, 13)
        T14x, T14y = getPosition(board, 14)
        T15x, T15y = getPosition(board, 15)
        topRow, bottomRow = 2, 3
        
        finalRowsReady = finalRsReady(T9x, T9y, T10x, T10y, T11x, T11y, T12x,
                                      T12y, T13x, T13y, T14x, T14y, T15x, T15y,
                                      blankx, blanky, topRow, bottomRow)

        if not finalRowsReady:
            thirdRowOrdered = readyToRotate(T9x, T9y, T10x, T10y, T11x, T11y,
                                            T12x, T12y, blankx, blanky, topRow,
                                            bottomRow)
            if not thirdRowOrdered:
                nextMove = order4('third', board)
                # ensure we don't get caught in an infinite loop:
                if nextMove == oppDirection(lastMove):
                    nextMove = continueDir(lastMove, blankx, blanky, topRow,
                                           bottomRow)
                return nextMove
            else:
                # Since finalRowsReady = False, the last 3 tiles are not yet
                # ordered and in place relative to the thirdRow tiles.
                nextMove = moveLast3Ts(T9x, T9y, T10x, T10y, T11x, T11y, T12x,
                                       T12y, T13x, T13y, T14x, T14y, T15x, T15y,
                                       blankx, blanky, lastMove)
                # a check against lastMove is done in moveLast3Ts()
                return nextMove        
        # the following check on board is needed so that once the board is
        # solved, hitting on the COMPUTE MOVE button will do nothing.
        elif finalRowsReady:
            if not(board == SOLVEDBOARD):
                # move blank CW or CCW
                clockwise= blankCW02(T9x, T9y, blankx, blanky)
                if clockwise:
                    nextMove = moveClockwise(blankx, blanky, topRow, bottomRow)
                    # ensure we don't get caught in an infinite loop:
                    if nextMove == oppDirection(lastMove):
                        nextMove = continueDir(lastMove, blankx, blanky,
                                               topRow, bottomRow)
                    return nextMove
                elif not clockwise:
                    nextMove = continueDirCCW(blankx, blanky, topRow, bottomRow)
                    # ensure we don't get caught in an infinite loop:
                    if nextMove == oppDirection(lastMove):
                        nextMove = continueDir(lastMove, blankx, blanky,
                                               topRow, bottomRow)
                    return nextMove
            elif board == SOLVEDBOARD:
                return None

##############################################################################
### helper ftns
##############################################################################

def adjacent4(Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx, Tdy, blankx, blanky):
    """Returns True if all of Ta - Td are contiguous except possibly for the
    presence of the blank.  Otherwise returns False.  This function expects
    the tiles to be in the correct rotation order."""
    returnVal = False
    # Are Ta and Tb contiguous?
    if adjacent2(Tax, Tay, Tbx, Tby, blankx, blanky):
        # Are Tb and Tc contiguous?
        if adjacent2(Tbx, Tby, Tcx, Tcy, blankx, blanky):
            # Are Tc and Td contiguous?
            if adjacent2(Tcx, Tcy, Tdx, Tdy, blankx, blanky):
                returnVal = True
    return returnVal


def blankCW(Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx, Tdy, blankx, blanky):
    """Returns True if we ought to move blank clockwise in the 2 rows by 4
    columns context.  When this ftn is called, all tiles are contiguous and
    ready for rotation into place."""
    returnVal = False
    # Case 1: Ta - Td are on same row; blank is above
    if (Tay == Tby and Tby == Tcy and Tcy == Tdy and blanky == Tay - 1):
        if blankx in (2, 3):
            returnVal = True
    # Case 2: Ta is above, remaining tiles below
    elif Tby == Tcy and Tcy == Tdy and Tay == Tby - 1 and Tax in (2, 3):
        returnVal = True
    # Case 3: Ta, Tb are above; Tc, Td below.  Note that Tb cannot be in col-1
    # since this would force Tc to be on topRow; Ta cannot be in col-0 for the
    # same reason.
    elif Tay == Tby and Tcy == Tdy and Tay == Tdy - 1 and Tbx in (2, 3):
        returnVal = True
    # Case 4: Td is below, remaining tiles above
    elif (Tay == Tby and Tby == Tcy and Tdy == Tay + 1 and Tcx in (2, 3)):
        returnVal = True
    return returnVal


def blankCW02(t9x, t9y, blankx, blanky):
    """Returns True if we ought to move blank clockwise when finishing up rows
    2 and 3."""
    returnVal = False
    if blanky == 2:  # topRow
        if t9y == 2 or (t9y == 3 and t9x == 3):
            returnVal = True
    elif blanky == 3:  # bottomRow
        if t9y == 2 and t9x in (1, 2, 3):
            returnVal = True
    return returnVal


def blankCW03(tx, ty, blankx, blanky):
    """Returns True if we ought to move blank clockwise when ordering the
    fourthRow tiles.  The tile argument will either be T13 or T14."""
    
    topRow, bottomRow = 2, 3

    returnVal = False
    if blanky == topRow:
        if blankx == 0:
            if (ty == bottomRow and tx in (0, 1)) or tx == 3:
                returnVal = True
        elif blankx in (1, 2):
            if tx in (0, 3):
                returnVal = True
        elif blankx == 3:
            if tx in (0, 3) or (tx, ty) == (2, topRow):
                returnVal = True
    elif blanky == bottomRow:
        if blankx == 0:
            if tx in (0, 3) or (tx, ty) == (1, bottomRow):
                returnVal = True
        elif blankx in (1, 2):
            if tx in (0, 3):
                returnVal = True
        elif blankx == 3:
            if tx in (0, 3) or (tx, ty) == (2, topRow):
                returnVal = True
    return returnVal


def moveClockwise(blankx, blanky, topRow, bottomRow):
    """Returns nextMove (one of UP, DOWN, LEFT, RIGHT) for rotating contiguous
    Ta - Td into their final positions, rotating in the clockwise direction.
    Context is 2 rows by 4 columns."""
    if blanky == topRow:
        if blankx in (0, 1, 2):
            return RIGHT
        elif blankx == 3:
            return DOWN
    elif blanky == bottomRow:
        if blankx in (1, 2, 3):
            return LEFT
        elif blankx == 0:
            return UP


def continueDir(lastMove, blankx, blanky, topRow, bottomRow):
    """Context is 2 rows by 4 columns.  Returns the next move for blank, 
    continuing in either a clockwise or counter-clockwise direction.  Note
    that this function will not work if we entered topRow or bottomRow
    from a swap column."""
    
    try:
        if blankx in (1, 2) and lastMove in (UP, DOWN):
            raise ValueError
    except ValueError:
        print("ERROR: Cannot call continueDir after having just done a cross-swap.")
    
    if blanky == topRow:
        if blankx == 0:
            if lastMove == LEFT:
                return DOWN
            elif lastMove == UP:
                return RIGHT
        elif blankx in (1, 2):
            if lastMove == RIGHT:
                return RIGHT
            elif lastMove == LEFT:
                return LEFT
        elif blankx == 3:
            if lastMove == RIGHT:
                return DOWN
            elif lastMove == UP:
                return LEFT
    elif blanky == bottomRow:
        if blankx == 0:
            if lastMove == DOWN:
                return RIGHT
            elif lastMove == LEFT:
                return UP
        elif blankx in (1, 2):
            if lastMove == RIGHT:
                return RIGHT
            elif lastMove == LEFT:
                return LEFT
        elif blankx == 3:
            if lastMove == RIGHT:
                return UP
            elif lastMove == DOWN:
                return LEFT


def readyToRotate(Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx, Tdy, blankx, blanky,
                  topRow, bottomRow):
    """Returns True if the ORDER among the tiles is such that we can rotate
    them into their final places once they have been made contiguous.  If we
    are working on tiles for the first row, a=1, b=2, c=3, d=4.  If we are
    working on tiles for the second row, a=5, b=6, c=7, and d=8.  If a set of
    tiles is readyToRotate but not contiguous, a call is made to makeAdjacent4.
       Although the tiles sent into this ftn might not be in the proper order,
    they will be in the rows we would need them to be in for rotation into
    their final spots.  Blank will also be located in either the topRow or
    bottomRow."""

    board_positions = {(0, topRow), (1, topRow), (2, topRow), (3, topRow),
                       (0, bottomRow), (1, bottomRow), (2, bottomRow),
                       (3, bottomRow)}
    remaining_positions = board_positions - {(Tax, Tay), (Tbx, Tby), (Tcx, Tcy),
                                             (Tdx, Tdy), (blankx, blanky)}
    remainder = list(remaining_positions)
    Qx, Qy = remainder[0][0], remainder[0][1]
    Rx, Ry = remainder[1][0], remainder[1][1]
    Sx, Sy = remainder[2][0], remainder[2][1]

    mylst = getTrueReversedTs(Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx, Tdy, blankx,
                              blanky, Qx, Qy, Rx, Ry, Sx, Sy, topRow, bottomRow)
    if len(mylst) == 0:
        return True
    else:
        return False


def finalRsReady(T9x, T9y, T10x, T10y, T11x, T11y, T12x, T12y, T13x, T13y,
                 T14x, T14y, T15x, T15y, blankx, blanky, topRow, bottomRow):
    """Returns True if the final two rows of the puzzle are ready to be
    rotated into place.  The rows are ready if the tiles are in order.  Because
    two rows of tiles are being considered at once, we will not have the
    correct order among the tiles unless we also have the tiles adjacent."""

    t9betw = tileBetw(T13x, T13y, T10x, T10y, T9x, T9y, blankx, blanky,
                       topRow, bottomRow)
    t10betw = tileBetw(T9x, T9y, T11x, T11y, T10x, T10y, blankx, blanky,
                       topRow, bottomRow)
    t11betw = tileBetw(T10x, T10y, T12x, T12y, T11x, T11y, blankx, blanky,
                       topRow, bottomRow)
    t12betw = tileBetw(T11x, T11y, T15x, T15y, T12x, T12y, blankx, blanky,
                       topRow, bottomRow)
    t13betw = tileBetw(T9x, T9y, T14x, T14y, T13x, T13y, blankx, blanky,
                       topRow, bottomRow)
    t14betw = tileBetw(T13x, T13y, T15x, T15y, T14x, T14y, blankx, blanky,
                       topRow, bottomRow)

    if (t9betw and t10betw and t11betw and t12betw and t13betw and t14betw):
        return True
    else:
        return False


def orderLast3Ts(T9x, T9y, T10x, T10y, T11x, T11y, T12x, T12y, Qx, Qy, Rx, Ry,
                 Sx, Sy, blankx, blanky):
    """Returns nextMove (one of UP, DOWN, LEFT, RIGHT) with goal of ordering
    the last 3 tiles (i.e., the fourthRow tiles).  Once ordered, all 7 tiles
    are ready to be rotated into their final positions.  Q = T13, R = T14, and
    S = T15.  When in the bottomRow, if the order of the tiles from left to
    right is Q, R, S, we are done.  The only other bottomRow permutations we
    can have are: (1) R, S, Q; and (2) S, Q, R.  The first requires only one
    cross-swap; the second permutation requires 2 cross-swaps."""

    topRow, bottomRow = 2, 3
    RbetwT9S = tileBetw(T9x, T9y, Sx, Sy, Rx, Ry, blankx, blanky, topRow, bottomRow)
    SbetwRQ = tileBetw(Rx, Ry, Qx, Qy, Sx, Sy, blankx, blanky, topRow, bottomRow)
    QbetwST12 = tileBetw(Sx, Sy, T12x, T12y, Qx, Qy, blankx, blanky, topRow, bottomRow)
    case1 = RbetwT9S and SbetwRQ and QbetwST12
    
    SbetwT9Q = tileBetw(T9x, T9y, Qx, Qy, Sx, Sy, blankx, blanky, topRow, bottomRow)
    QbetwSR = tileBetw(Sx, Sy, Rx, Ry, Qx, Qy, blankx, blanky, topRow, bottomRow)
    RbetwQT12 = tileBetw(Qx, Qy, T12x, T12y, Rx, Ry, blankx, blanky, topRow, bottomRow)
    case2 = SbetwT9Q and QbetwSR and RbetwQT12

    # the following is needed to measure the solution space    
    if not(case1 or case2):
        return 'Stop'
    
    if case1:
        # permutation is R,S,Q in the bottomRow, from left to right
        # single cross-swap is required: Q in topRow with R,S in an outer column
        
        # first see if cross-swap conditions are met
        if blanky == bottomRow and blankx == 2 and Qy == topRow and Qx == 2:
            return UP
        elif blanky == topRow and blankx == 1 and Qy == bottomRow and Qx == 1:
            return DOWN
        else:
            clockwise = blankCW03(Qx, Qy, blankx, blanky)
            if clockwise:
                nextMove = moveClockwise(blankx, blanky, topRow, bottomRow)
                return nextMove
            else:
                nextMove = continueDirCCW(blankx, blanky, topRow, bottomRow)
                return nextMove
    elif not case1:
        # permutation is S,Q,R in the bottomRow, from left to right
        # 2 cross-swaps are required: first: R in topRow with S,Q in an outer column
        
        # first see if cross-swap conditions are met
        if blanky == bottomRow and blankx == 2 and Ry == topRow and Rx == 2:
            return UP
        elif blanky == topRow and blankx == 1 and Ry == bottomRow and Rx == 1:
            return DOWN
        else:
            clockwise = blankCW03(Rx, Ry, blankx, blanky)
            if clockwise:
                nextMove = moveClockwise(blankx, blanky, topRow, bottomRow)
                return nextMove
            else:
                nextMove = continueDirCCW(blankx, blanky, topRow, bottomRow)
                return nextMove


def putLast3betw(T9x, T9y, T10x, T10y, T11x, T11y, T12x, T12y, Qx, Qy,
                 Rx, Ry, Sx, Sy, blankx, blanky):
    """Returns nextMove (one of UP, DOWN, LEFT, RIGHT) with goal of moving the
    last 3 tiles (Q, R, S) betw T9 and T12."""
    
    # Move Q,R,S into place betw Ta and Td
    topRow, bottomRow = 2, 3
       
    # First see if a cross-swap can be made.  Need one of Q,R,S in a swap
    # column with Ta, Td on either side of blank.
    if blanky == bottomRow and blankx == 1 and T9x < blankx and T12x > blankx:
        if anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, topRow)):
            return UP
    elif blanky == bottomRow and blankx == 2 and T9x < blankx and T12x > blankx:
        if anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, topRow)):
            return UP
    elif blanky == topRow and blankx == 1 and T9x > blankx and T12x < blankx:
        if anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, bottomRow)):
            return DOWN
    elif blanky == topRow and blankx == 2 and T9x > blankx and T12x < blankx:
        if anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, bottomRow)):
            return DOWN

    # Special logic is required when one of Q,R,S is in each of the gaps, i.e.,
    # when TaTb_cont, TbTc_cont, and TcTd_cont are all false.  When this
    # scenario occurs, we can rotate blank through the tiles and never have
    # the above cross-swap conditions met.
    TaTb_cont = False
    if adjacent2(T9x, T9y, T10x, T10y, blankx, blanky):
        TaTb_cont = True
    TbTc_cont = False
    if adjacent2(T10x, T10y, T11x, T11y, blankx, blanky):
        TbTc_cont = True
    TcTd_cont = False
    if adjacent2(T11x, T11y, T12x, T12y, blankx, blanky):
        TcTd_cont = True
    
    if TaTb_cont == False and TbTc_cont == False and TcTd_cont == False:
        nextMove = move3NotDoneSpecial(T9x, T9y, T10x, T10y, T11x, T11y, T12x, T12y,
                                       blankx, blanky, Qx, Qy, Rx, Ry, Sx, Sy,
                                       topRow, bottomRow)
        return nextMove

    if T12y == topRow:
        if T12x == 0:
            if blanky == topRow:
                if blankx == 1:
                    if (T9x == 3 and (anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, bottomRow)) or
                                      anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (0, bottomRow)))):
                        return RIGHT
                    else:
                        return LEFT  # default dir = CCW
                elif blankx == 2:
                    if (T9x == 3 and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (0, bottomRow)) and
                        not anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, bottomRow))):
                        return RIGHT
                    else:
                        return LEFT  # default dir = CCW
                elif blankx == 3:
                    if (T9x in (2, 3) and
                        anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (0, bottomRow)) and
                        not anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, bottomRow)) and
                        not anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, bottomRow))):
                        return DOWN
                    else:
                        return LEFT  # default dir = CCW
            elif blanky == bottomRow:
                if blankx == 0:
                    if ((T9x > 1 and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, bottomRow))) or
                        (T9x == 3 and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, bottomRow)))):
                        return UP
                    else:
                        return RIGHT  # default dir = CCW
                elif blankx == 1:
                    if ((T9x > 1 and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (0, bottomRow))) or
                        (T9x == 3 and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, bottomRow)))):
                        return LEFT
                    else:
                        return RIGHT  # default dir = CCW
                elif blankx == 2:
                    if ((T9x > 1 and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (0, bottomRow))) or
                        (T9x == 3 and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, bottomRow)))):
                        return LEFT
                    else:
                        return RIGHT  # default dir = CCW
                elif blankx == 3:
                    if ((T9x > 1 and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (0, bottomRow))) or
                        (T9x == 3 and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, bottomRow)))):
                        return LEFT
                    else:
                        return UP  # default dir = CCW
        elif T12x == 1:
            if blanky == topRow:
                if blankx == 0:
                    if (anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, bottomRow)) or
                        (T9x == 3 and
                         anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, bottomRow)))):
                        return RIGHT
                    else:
                        return DOWN  # default dir = CCW
                elif blankx == 2:
                    if (T9y == bottomRow and T9x in (2, 3) and
                        (anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, bottomRow)) or
                         anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (0, bottomRow)))):
                        return RIGHT
                    else:
                        return LEFT  # default dir = CCW
                elif blankx == 3:
                    if (not anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, bottomRow)) and
                        ((T9x in (2, 3) and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (0, bottomRow))) or
                        (T9y == bottomRow and T9x in (2, 3) and 
                         anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, bottomRow))))):
                        return DOWN
                    else:
                        return LEFT  # default dir = CCW
            elif blanky == bottomRow:
                if blankx == 0:
                    if (anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, bottomRow)) or
                        (T9x == 3 and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, bottomRow)))):
                        return UP
                    else:
                        return RIGHT  # default dir = CCW
                elif blankx == 1:
                    if (anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (0, bottomRow)) or
                        (T9x == 3 and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, bottomRow)))):
                        return LEFT
                    else:
                        return RIGHT  # default dir = CCW
                elif blankx == 2:
                    if (anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (0, bottomRow)) or
                        (T9x == 3 and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, bottomRow)))):
                        return LEFT
                    else:
                        return RIGHT  # default dir = CCW
                elif blankx == 3:
                    if (anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (0, bottomRow)) or
                        (T9x == 3 and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, bottomRow)))):
                        return LEFT
                    else:
                        return UP  # default dir = CCW
        elif T12x == 2:
            if blanky == topRow:
                if blankx == 0:
                    if anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, bottomRow)):
                        return RIGHT
                    else:
                        return DOWN  # default dir = CCW
                elif blankx == 1:
                    if anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, bottomRow)):
                        return RIGHT
                    else:
                        return LEFT  # default dir = CCW
                elif blankx == 3:
                    if anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, bottomRow)):
                        return DOWN
                    else:
                        return LEFT  # default dir = CCW
            elif blanky == bottomRow:
                if blankx == 0:
                    if anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, bottomRow)):
                        return UP
                    else:
                        return RIGHT  # default dir = CCW
                elif blankx == 1:
                    if anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, bottomRow)):
                        return LEFT
                    else:
                        return RIGHT  # default dir = CCW
                elif blankx == 2:
                    if anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, bottomRow)):
                        return LEFT
                    else:
                        return RIGHT  # default dir = CCW
                elif blankx == 3:
                    if anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, bottomRow)):
                        return LEFT
                    else:
                        return UP  # default dir = CCW
        elif T12x == 3:
            if blanky == topRow:
                if blankx == 0:
                    return DOWN  # default dir = CCW
                elif blankx in (1, 2):
                    return LEFT  # default dir = CCW
            elif blanky == bottomRow:
                if blankx in (0, 1):
                    return RIGHT  # default dir = CCW
                elif blankx == 2:
                    if ((T9x, T9y) == (0, bottomRow) and
                        anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, topRow))):
                        return LEFT
                    else:
                        return RIGHT  # default dir = CCW
                elif blankx == 3:
                    if ((T9x < 2 and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, topRow))) or
                        ((T9x, T9y) == (0, bottomRow) and
                         anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, topRow)))):
                        return LEFT
                    else:
                        return UP  # default dir = CCW
    elif T12y == bottomRow:
        if T12x == 0:
            if blanky == topRow:
                if blankx == 0:
                    if ((T9x > 1 and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, bottomRow))) or
                        (T9x == 3 and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, bottomRow)))):
                        return RIGHT
                    else:
                        return DOWN  # default dir = CCW
                elif blankx == 1:
                    if T9x == 3 and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, bottomRow)):
                        return RIGHT
                    else:
                        return LEFT  # default dir = CCW
                elif blankx in (2, 3):
                    return LEFT  # default dir = CCW
            elif blanky == bottomRow:
                if blankx in (1, 2):
                    return RIGHT  # default dir = CCW
                elif blankx == 3:
                    return UP  # default dir = CCW
        elif T12x == 1:
            if blanky == topRow:
                if blankx == 0:
                    if T9x == 0 and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, topRow)):
                        return RIGHT
                    else:
                        return DOWN  # default dir = CCW
                elif blankx == 1:
                    if T9x == 0 and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, topRow)):
                        return RIGHT
                    else:
                        return LEFT  # default dir = CCW
                elif blankx == 2:
                    if T9x == 0 and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, topRow)):
                        return RIGHT
                    else:
                        return LEFT  # default dir = CCW
                elif blankx == 3:
                    if T9x == 0 and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, topRow)):
                        return DOWN
                    else:
                        return LEFT  # default dir = CCW
            elif blanky == bottomRow:
                if blankx == 0:
                    if T9x < 2 and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, topRow)):
                        return UP
                    else:
                        return RIGHT  # default dir = CCW
                elif blankx == 2:
                    if T9x == 0 and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, topRow)):
                        return LEFT
                    else:
                        return RIGHT  # default dir = CCW
                elif blankx == 3:
                    if T9x == 0 and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, topRow)):
                        return LEFT
                    else:
                        return UP  # default dir = CCW
        elif T12x == 2:
            if blanky == topRow:
                if blankx == 0:
                    if anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (3, topRow)):
                        return RIGHT
                    else:
                        return DOWN  # default dir = CCW
                elif blankx in (1, 2):
                    if anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (3, topRow)):
                        return RIGHT
                    else:
                        return LEFT  # default dir = CCW
                elif blankx == 3:
                    if anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, topRow)):
                        return DOWN
                    else:
                        return LEFT  # default dir = CCW
            elif blanky == bottomRow:
                if blankx == 0:
                    if (anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (3, topRow)) and
                        not anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, topRow))):
                        return UP
                    else:
                        return RIGHT  # default dir = CCW
                elif blankx == 1:
                    if anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (3, topRow)):
                        return LEFT
                    else:
                        return RIGHT  # default dir = CCW
                elif blankx == 3:
                    if(anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, topRow)) or
                       (T9x == 0 and
                        anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, topRow)))):
                        return LEFT
                    else:
                        return UP  # default dir = CCW
        elif T12x == 3:
            if blanky == topRow:
                if blankx == 0:
                    if((anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (3, topRow)) and T9x < 2) or
                       (T9x == 0 and
                        anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, topRow)))):
                        return RIGHT
                    else:
                        return DOWN  # default dir = CCW
                elif blankx == 1:
                    if((anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (3, topRow)) and T9x < 2) or
                       (T9x == 0 and
                        anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, topRow)))):
                        return RIGHT
                    else:
                        return LEFT  # default dir = CCW
                elif blankx == 2:
                    if((anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (3, topRow)) and T9x < 2) or
                       (T9x == 0 and
                        anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, topRow)))):
                        return RIGHT
                    else:
                        return LEFT  # default dir = CCW
                elif blankx == 3:
                    if((anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, topRow)) and T9x < 2) or
                       (T9x == 0 and
                        anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, topRow)))):
                        return DOWN
                    else:
                        return LEFT  # default dir = CCW
            elif blanky == bottomRow:
                if blankx == 0:
                    if ((anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (3, topRow)) and T9x < 2) or
                        (T9x == 0 and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, topRow)))):
                        return UP
                    else:
                        return RIGHT  # default dir = CCW
                elif blankx == 1:
                    if ((T9x == 0 and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (3, topRow))) or
                        ((T9x, T9y) == (0, topRow) and
                         anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, topRow)))):
                        return LEFT
                    else:
                        return RIGHT  # default dir = CCW
                elif blankx == 2:
                    if (T9x == 0 and (anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, topRow)) or
                                      anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (3, topRow)))):
                        return LEFT
                    else:
                        return RIGHT


def moveLast3Ts(T9x, T9y, T10x, T10y, T11x, T11y, T12x, T12y, T13x, T13y, T14x,
                T14y, T15x, T15y, blankx, blanky, lastMove):
    """Returns nextMove (one of UP, DOWN, LEFT, RIGHT) with goal of moving the
    final 3 tiles into place so that they can be rotated with the thirdRow
    tiles into their final positions.  The thirdRow tiles are already in the
    correct order.  The next step is to get the last 3 tiles betw Ta (T9) and
    Td (T12).  Once that is done, they can be put into the correct order.
    After that, the rotation ftn can be called."""
    
    topRow, bottomRow = 2, 3
    # Before we can order the last 3 tiles, we need to make sure they are all
    # betw Ta (T9) and Td (T12).  The latter will be true if each of the
    # following tests is true.
    TaTb_adj = adjacent2(T9x, T9y, T10x, T10y, blankx, blanky)
    TbTc_adj = adjacent2(T10x, T10y, T11x, T11y, blankx, blanky)
    TcTd_adj = adjacent2(T11x, T11y, T12x, T12y, blankx, blanky)
   
    if TaTb_adj and TbTc_adj and TcTd_adj:
        # If the thirdRow tiles are adjacent, the fourthRow tiles are situated
        # betw Ta and Td.
        t13betw = tileBetw(T9x, T9y, T14x, T14y, T13x, T13y, blankx, blanky,
                           topRow, bottomRow)
        t14betw = tileBetw(T13x, T13y, T15x, T15y, T14x, T14y, blankx, blanky,
                           topRow, bottomRow)
        t15betw = tileBetw(T14x, T14y, T12x, T12y, T15x, T15y, blankx, blanky,
                           topRow, bottomRow)
        ordered = t13betw and t14betw and t15betw
        
        if not ordered:
            nextMove = orderLast3Ts(T9x, T9y, T10x, T10y, T11x, T11y, T12x,
                                    T12y, T13x, T13y, T14x, T14y, T15x, T15y,
                                    blankx, blanky)
            if nextMove == oppDirection(lastMove):
                nextMove = continueDir(lastMove, blankx, blanky, topRow, bottomRow)
            return nextMove
        else:
            return None
    else:
        # Move the fourthRow tiles betw T9 and T12.
        nextMove = putLast3betw(T9x, T9y, T10x, T10y, T11x, T11y, T12x, T12y,
                                T13x, T13y, T14x, T14y, T15x, T15y, blankx, blanky)
        if nextMove == oppDirection(lastMove):
            nextMove = continueDir(lastMove, blankx, blanky, topRow, bottomRow)
        return nextMove


##############################################################################
###
##############################################################################
