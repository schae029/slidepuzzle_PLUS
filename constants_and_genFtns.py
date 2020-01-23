# -*- coding: utf-8 -*-
"""
@author: Greg Schaefer

module: constants_and_genFtns.py

module contents (5 ftns + 8 constants):

    - getPosition (written by Al Sweigart)
    - oppDirection
    - blankBetw
    - adjacent2
    - anyQRSinCell
    

Released under a GNU GPLv3 license. 

"""

#############################################################################
### constants_and_genFtns.py COPYRIGHT:
#############################################################################

# SlidePuzzlePlus, constants_and_genFtns.py
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

#############################################################################
### constants (all are from Al Sweigart's Slide Puzzle code)
#############################################################################

BOARDWIDTH = 4  # number of columns in the board
BOARDHEIGHT = 4  # number of rows in the board

BLANK = None
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
SOLVED = 'Solved!'

#############################################################################
### general ftns used in several slidePuzzle modules
#############################################################################

# getPosition was written by Al Sweigart
def getPosition(board, tileVal):
    # Return the x and y of board coordinates for the given tile.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == tileVal:
                return (x, y)


def oppDirection(direction):
    """Returns the opposite direction of 'direction'."""
    if direction == UP:
        return DOWN
    elif direction == DOWN:
        return UP
    elif direction == RIGHT:
        return LEFT
    elif direction == LEFT:
        return RIGHT


def blankBetw(Tax, Tay, Tbx, Tby, blankx, blanky):
    """ Returns True if the blank is the only tile between Ta and Tb.
    Otherwise returns False.  This function does not consider whether the
    tiles are in the proper order based on the row(s) they are in.
    This function is called by adjacent2."""

    returnVal = False
    # Case 1: Ta is to left of Tb; Ta, Tb, and blank are on same row
    if Tbx > Tax and Tay == Tby and Tby == blanky:
        if blankx - 1 == Tax and blankx + 1 == Tbx:
            returnVal = True
    # Case 2: Ta is to right of Tb; Ta, Tb, and blank are on same row
    elif Tax > Tbx and Tay == Tby and Tby == blanky:
        if blankx - 1 == Tbx and blankx + 1 == Tax:
            returnVal = True
    # Case 3: Ta is above Tb and blank is to left of Ta
    elif Tay == Tby - 1 and Tay == blanky and blankx == 0:
        if Tbx == 0 and Tax == Tbx + 1:
            returnVal = True
    # Case 4: Ta is above Tb, blank is to right of Ta
    elif Tay == Tby - 1 and Tay == blanky and blankx == 3:
        if Tbx == 3 and Tax == Tbx - 1:
            returnVal = True
    # Case 5: Ta is above Tb and blank is to left of Tb
    elif Tay == Tby - 1 and Tby == blanky and blankx == 0:
        if Tax == 0 and Tax == Tbx - 1:
            returnVal = True
    # Case 6: Ta is above Tb and blank is to right of Tb
    elif Tay == Tby - 1 and Tby == blanky and blankx == 3:
        if Tax == 3 and Tax == Tbx + 1:
            returnVal = True
    # Case 7: Tb is above Ta and blank is to left of Tb
    elif Tby == Tay - 1 and Tby == blanky and blankx == 0:
        if Tax == 0 and Tbx == Tax + 1:
            returnVal = True
    # Case 8: Tb is above Ta, blank is to right of Tb
    elif Tby == Tay - 1 and Tby == blanky and blankx == 3:
        if Tax == 3 and Tbx == Tax - 1:
            returnVal = True
    # Case 9: Tb is above Ta and blank is to left of Ta
    elif Tby == Tay - 1 and Tay == blanky and blankx == 0:
        if Tbx == 0 and Tbx == Tax - 1:
            returnVal = True
    # Case 10: Tb is above Ta and blank is to right of Ta
    elif Tby == Tay - 1 and Tay == blanky and blankx == 3:
        if Tbx == 3 and Tbx == Tax + 1:
            returnVal = True
    return returnVal


def adjacent2(Tax, Tay, Tbx, Tby, blankx, blanky):
    """Returns True if Ta and Tb are contiguous, blank excepted.  This ftn
    does not require that Ta and Tb be in the order required for rotation into
    their final places."""
    returnVal = False
    if ((abs(Tax - Tbx) == 1 and Tay == Tby) or
        (Tax == Tbx and abs(Tay - Tby) == 1 and (Tax == 0 or Tax == 3)) or
        blankBetw(Tax, Tay, Tbx, Tby, blankx, blanky)):
        returnVal = True
    return returnVal


def anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, cell):
    """Returns True if any of Q,R,S is in the given cell.  'cell' is a tuple in
    (col, row) format."""
    if Qy == cell[1] and Qx == cell[0]:
        return True
    elif Ry == cell[1] and Rx == cell[0]:
        return True
    elif Sy == cell[1] and Sx == cell[0]:
        return True
    else:
        return False

#############################################################################
### 
#############################################################################
