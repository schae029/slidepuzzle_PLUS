# -*- coding: utf-8 -*-
"""
@author: Greg Schaefer

module name: makeAjacent4.py

module contents (7 ftns):

    - tileBetwTaTd
    - tileBetw
    - makeAdjacent4
    - moveOneNotDone
    - moveTwoNotDone
    - moveThreeNotDone
    - move3NotDoneSpecial


Released under a GNU GPLv3 license. 

"""

#############################################################################
### makeAdjacent4.py COPYRIGHT:
#############################################################################

# SlidePuzzlePlus, makeAdjacent4.py
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

#############################################################################
### makeAdjacent4
#############################################################################

from constants_and_genFtns import *

#############################################################################
### Helper ftns
#############################################################################

def tileBetwTaTd(Tax, Tay, Tdx, Tdy, testx, testy, topRow, bottomRow):
    """ Returns True if the 'test' tile is between Ta and Td when all tiles are
    in the 2 rows by 4 columns context.  Here 'test' will be one of the Q,R,S
    tiles from makeAdjacent4.  Since Ta and Td will already be in the order 
    required for rotation into place, we can correctly determine whether the
    test tile is between Ta and Td, i.e., where it needs to be in order for Ta, 
    Tb, Tc, and Td to be made adjacent.  If all of Q,R,S are betw Ta and Td,
    this ftn won't be called since Ta - Td will already be adjacent.  So when
    this ftn is called, we have at most two of Q,R,S betw Ta,Td.  This in turn
    means that we can have 3 tiles at most between Ta and Td when this ftn
    returns True.  (The third tile would be the blank.)"""

    returnVal = False
    # Case 1: all tiles in topRow (forcing Ta to be to right of Td)
    if Tax > Tdx + 1 and Tay == topRow and Tdy == topRow and testy == topRow:
        if testx > Tdx and testx < Tax:
            returnVal = True
    # Case 2: all tiles in bottomRow (forcing Ta to be to left of Td)
    elif (Tax < Tdx - 1 and Tay == bottomRow and Tdy == bottomRow and
          testy == bottomRow):
        if testx > Tax and testx < Tdx:
            returnVal = True
    #################################################################
    # Td in topRow, Ta in bottomRow:
    elif Tay == bottomRow and Tdy == topRow:
        if Tdx == 0:
            if Tax == 3 and testy == topRow:
                returnVal = True
        elif Tdx == 1:
            if Tax == 3 and testy == topRow and testx > Tdx:
                returnVal = True
            elif Tax == 2 and testx >= Tax:
                returnVal = True
        elif Tdx == 2:
            if Tax in (2, 3) and testx > Tdx:
                returnVal = True
            elif Tax == 1 and testx > Tax:
                returnVal = True
        elif Tdx == 3:
            if testy == bottomRow and testx > Tax:
                returnVal = True
    #################################################################
    # Td in bottomRow, Ta in topRow:
    elif Tay == topRow and Tdy == bottomRow:
        if Tax == 0:
            if testy == bottomRow and testx < Tdx:
                returnVal = True
        elif Tax == 1:
            if Tdx == 0 and testy == topRow and testx < Tax:
                returnVal = True
            elif Tdx in (1, 2) and testx < Tdx:
                returnVal = True
        elif Tax == 2:
            if Tdx == 0 and testy == topRow and testx < Tax:
                returnVal = True
            elif Tdx == 1 and testx < Tax:
                returnVal = True
        elif Tax == 3:
            if Tdx == 0 and testy == topRow:
                returnVal = True
    return returnVal


def tileBetw(T1x, T1y, T2x, T2y, testx, testy, blankx, blanky, topRow, bottomRow):
    """Returns True if the test tile is betw T1 and T2.  The blank can also be
    betw T1 and T2.  This ftn is primarily used by moveOneNotDone.  T1 and T2
    do NOT need to be in their proper rotation order.  Other than test and blank,
    no other tile can be betw. T1 and T2; otherwise this ftn returns False.
    It is exactly because test and blank can be the only tiles betw T1 and T2
    that we cannot make use of this ftn to do the work that tileBetwTaTd does
    for us; the latter allows there to be several tiles betw Ta and Td."""

    returnVal = False
    # T2 in topRow
    if T2y == topRow:
        if T2x == 0 and T1y == bottomRow and testy == bottomRow:
            if T1x == 1 and testx == 0:
                returnVal = True
            elif (T1x == 2 and blanky == bottomRow and blankx in (0, 1) and
                  testx in (0, 1)):
                returnVal = True
        elif T2x == 1 and T1y == bottomRow:
            if T1x == 0 and testx == 0:
                returnVal = True
            elif T1x == 1 and testx == 0 and blankx == 0:
                returnVal = True
        elif T2x == 2 and testy == topRow and T1x == 0:
            if T1y == topRow and testx == 1:
                returnVal = True
            elif (T1y == bottomRow and testx in (0, 1) and blanky == topRow and
                  blankx in (0, 1)):
                returnVal = True
        elif T2x == 3 and T1y == topRow:
            if T1x == 1 and testy == topRow and testx == 2:
                returnVal = True
            elif (T1x == 0 and testy == topRow and testx in (1, 2) and
                  blanky == topRow and blankx in (1, 2)):
                returnVal = True
    # T2 in bottomRow
    elif T2y == bottomRow:
        if T2x == 0 and T1y == bottomRow and testy == bottomRow:
            if T1x == 2 and testx == 1:
                returnVal = True
            elif (T1x == 3 and testx in (1, 2) and blanky == bottomRow and
                  blankx in (1, 2)):
                returnVal = True
        elif T2x == 1 and T1x == 3 and testy == bottomRow:
            if T1y == bottomRow and testx == 2:
                returnVal = True
            elif (T1y == topRow and testx in (2, 3) and blanky == bottomRow and
                  blankx in (2, 3)):
                returnVal = True
        elif T2x == 2 and T1y == topRow and testx == 3:
            if T1x == 3 and testy == bottomRow:
                returnVal = True
            elif (T1x == 2 and blankx == 3 and blanky in (topRow, bottomRow) and
                  testy in (topRow, bottomRow)):
                returnVal = True
        elif T2x == 3 and T1y == topRow and testy == topRow:
            if T1x == 2 and testx == 3:
                returnVal = True
            elif (T1x == 1 and testx in (2, 3) and blanky == topRow and
                  blankx in (2, 3)):
                returnVal = True

    if returnVal == False:
        # run the same code as above, but exchange T1 for T2 and vice versa
        T3x, T3y = T2x, T2y
        T2x, T2y = T1x, T1y
        T1x, T1y = T3x, T3y
        # T2 in topRow
        if T2y == topRow:
            if T2x == 0 and T1y == bottomRow and testy == bottomRow:
                if T1x == 1 and testx == 0:
                    returnVal = True
                elif (T1x == 2 and blanky == bottomRow and blankx in (0, 1) and
                      testx in (0, 1)):
                    returnVal = True
            elif T2x == 1 and T1y == bottomRow:
                if T1x == 0 and testx == 0:
                    returnVal = True
                elif T1x == 1 and testx == 0 and blankx == 0:
                    returnVal = True
            elif T2x == 2 and testy == topRow and T1x == 0:
                if T1y == topRow and testx == 1:
                    returnVal = True
                elif (T1y == bottomRow and testx in (0, 1) and blanky == topRow and
                      blankx in (0, 1)):
                    returnVal = True
            elif T2x == 3 and T1y == topRow:
                if T1x == 1 and testy == topRow and testx == 2:
                    returnVal = True
                elif (T1x == 0 and testy == topRow and testx in (1, 2) and
                      blanky == topRow and blankx in (1, 2)):
                    returnVal = True
        # T2 in bottomRow
        elif T2y == bottomRow:
            if T2x == 0 and T1y == bottomRow and testy == bottomRow:
                if T1x == 2 and testx == 1:
                    returnVal = True
                elif (T1x == 3 and testx in (1, 2) and blanky == bottomRow and
                      blankx in (1, 2)):
                    returnVal = True
            elif T2x == 1 and T1x == 3 and testy == bottomRow:
                if T1y == bottomRow and testx == 2:
                    returnVal = True
                elif (T1y == topRow and testx in (2, 3) and blanky == bottomRow and
                      blankx in (2, 3)):
                    returnVal = True
            elif T2x == 2 and T1y == topRow and testx == 3:
                if T1x == 3 and testy == bottomRow:
                    returnVal = True
                elif (T1x == 2 and blankx == 3 and blanky in (topRow, bottomRow) and
                      testy in (topRow, bottomRow)):
                    returnVal = True
            elif T2x == 3 and T1y == topRow and testy == topRow:
                if T1x == 2 and testx == 3:
                    returnVal = True
                elif (T1x == 1 and testx in (2, 3) and blanky == topRow and
                      blankx in (2, 3)):
                    returnVal = True
    return returnVal

#############################################################################
### Main functions for makeAdjacent4.py:
#############################################################################


def makeAdjacent4(Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx, Tdy, blankx, blanky):
    """Returns nextMove value.  At this point the tiles are in the correct rows
    and order for rotation into their final places, only one or more non-blank
    tiles lie between either (Ta, Tb), (Tb, Tc), or (Tc, Td).  We need Ta, Tb,
    Tc, and Td to be separated only by the blank, or no tile at all, before we
    can begin rotating the row into place.  We want the non-blank tiles that
    are not Ta, Tb, Tc, or Td to end up between Td and Ta; below I refer to 
    these non-blank tiles as Q, R, and S.
    The check to ensure we do not get caught in an infinite loop is done in
    the calling function, getNextMove."""

    # Get the rows we are working with.  There will be exactly two rows.
    rows = {Tay, Tby, Tcy, Tdy, blanky}
    rows_list = list(rows)
    row1, row2 = rows_list[0], rows_list[1]
    # Note that coordinate reference for board positions is by (column, row)
    # and not (row, column).  The x-coordinate tells us the column; the
    # y-coordinate tells us the row.
    board_positions = {(0, row1), (1, row1), (2, row1), (3, row1), (0, row2),
                       (1, row2), (2, row2), (3, row2)}
    remaining_positions = board_positions - {(Tax, Tay), (Tbx, Tby), (Tcx, Tcy),
                                             (Tdx, Tdy), (blankx, blanky)}
    # To make Ta - Td adjacent, we must move Q, R, and S betw. Ta and Td.
    # Get the locations of Q, R, and S.
    remainder = list(remaining_positions)
    Qx, Qy = remainder[0][0], remainder[0][1]
    Rx, Ry = remainder[1][0], remainder[1][1]
    Sx, Sy = remainder[2][0], remainder[2][1]
    
    if row1 < row2:
        topRow = row1
        bottomRow = row2
    else:
        topRow = row2
        bottomRow = row1

    # First determine whether a "preferred" swap can be done.  If so, execute
    # the cross-swap.
    if (blanky == bottomRow and blankx in (1, 2) and Tdx > blankx and
        Tax < blankx):
        if Qx == blankx or Rx == blankx or Sx == blankx:
            return UP
    # NOTE: when inserting Q,R,S betw. Ta and Td, pull them into bottomRow if
    # possible.  When there is only one of Q,R,S remaining to be "swapped", the
    # swap move should always be UP.  Otherwise we can end up with Q,R,S all
    # betw. Ta,Td but in the topRow, where Ta-Td go---forcing a large number
    # of moves to rotate Ta-Td into place.

    # Find out if any of Q,R,S are betw. Ta, Td
    Qdone, Rdone, Sdone = False, False, False
    if tileBetwTaTd(Tax, Tay, Tdx, Tdy, Qx, Qy, topRow, bottomRow):
        Qdone = True
    if tileBetwTaTd(Tax, Tay, Tdx, Tdy, Rx, Ry, topRow, bottomRow):
        Rdone = True
    if tileBetwTaTd(Tax, Tay, Tdx, Tdy, Sx, Sy, topRow, bottomRow):
        Sdone = True
    # Find out how many of Q,R,S are not yet done
    oneNotDone = False
    threeNotDone = False
    twoNotDone = False
    if not Qdone and not Rdone and not Sdone:
        threeNotDone = True
    elif threeNotDone == False:
        if ((not Qdone and not Rdone) or (not Rdone and not Sdone) or
            (not Sdone and not Qdone)):
            twoNotDone = True
        elif twoNotDone == False:
            # makeAdjacent4 is called only when at least one of Q,R,S is out
            # of place
            oneNotDone = True
            
    # Address oneNotDone == True, knowing that we are not yet ready for a
    # preferred swap.
    if oneNotDone:
        if not Qdone:
            notDone_x, notDone_y = Qx, Qy
        elif not Rdone:
            notDone_x, notDone_y = Rx, Ry
        elif not Sdone:
            notDone_x, notDone_y = Sx, Sy
        nextMove = moveOneNotDone(Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx, Tdy,
                                  blankx, blanky, notDone_x, notDone_y,
                                  topRow, bottomRow)
        return nextMove
    # "non-preferred" swaps are allowed in moveTwoNotDone
    elif twoNotDone:
        if not Qdone and not Rdone:
            notDone1_x, notDone1_y = Qx, Qy
            notDone2_x, notDone2_y = Rx, Ry
        elif not Rdone and not Sdone:
            notDone1_x, notDone1_y = Rx, Ry
            notDone2_x, notDone2_y = Sx, Sy
        elif not Sdone and not Qdone:
            notDone1_x, notDone1_y = Sx, Sy
            notDone2_x, notDone2_y = Qx, Qy
        nextMove = moveTwoNotDone(Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx, Tdy,
                                  blankx, blanky, notDone1_x, notDone1_y,
                                  notDone2_x, notDone2_y, topRow, bottomRow)
        return nextMove
    # "non-preferred" swaps are allowed in moveThreeNotDone
    elif threeNotDone:
        nextMove = moveThreeNotDone(Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx, Tdy,
                                    blankx, blanky, Qx, Qy, Rx, Ry, Sx, Sy,
                                    topRow, bottomRow)
        return nextMove


def moveOneNotDone(Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx, Tdy, blankx, blanky,
                   notDone_x, notDone_y, topRow, bottomRow):
    """Returns nextMove (one of UP, DOWN, RIGHT, LEFT) for the case when there
    is still one of Q,R,S (see makeAdjacent4) to be moved betw Ta,Td.  If this
    ftn is called, the tile arrangement is such that we are not yet ready for
    a preferred cross-swap."""

    # look for quickest way to place the notDone tile in the topRow in a swap
    # column (1, 2).  If we do not insert, or swap, the notDone tile into the
    # bottomRow, there is a significant cost rotating Ta-Td into their final spots.
    betwTaTb = tileBetw(Tax, Tay, Tbx, Tby, notDone_x, notDone_y, blankx,
                        blanky, topRow, bottomRow)
    betwTbTc = tileBetw(Tbx, Tby, Tcx, Tcy, notDone_x, notDone_y, blankx,
                        blanky, topRow, bottomRow)
    betwTcTd = tileBetw(Tcx, Tcy, Tdx, Tdy, notDone_x, notDone_y, blankx,
                        blanky, topRow, bottomRow)

    # The gap in which the tile is located matters.  Separate logic is
    # required for the case where the tile is betw. Tc and Td.
    if betwTaTb or betwTbTc:
        if notDone_y == topRow:
            if notDone_x == 0:
                if blanky == topRow:
                    return LEFT
                elif blanky == bottomRow:
                    if blankx in (0, 1, 2):
                        return RIGHT
                    else:
                        return UP
            elif notDone_x == 1:
                if blanky == topRow:
                    if blankx in (0, 3):
                        return DOWN
                    elif blankx == 2:
                        return RIGHT
                elif blanky == bottomRow:
                    if blankx in (2, 3):
                        return LEFT
                    elif blankx == 0:
                        return RIGHT
            elif notDone_x == 2:
                if blanky == topRow:
                    if blankx in (0, 1):
                        return RIGHT
                    elif blankx == 3:
                        return DOWN
                elif blanky == bottomRow:
                    if blankx in (1, 2, 3):
                        return LEFT
                    elif blankx == 0:
                        return UP
            elif notDone_x == 3:
                if blanky == topRow:
                    return RIGHT
                elif blanky == bottomRow:
                    if blankx in (1, 2, 3):
                        return LEFT
                    else:
                        return UP
        # notDone in bottomRow:
        elif notDone_y == bottomRow:
            if notDone_x == 0:
                if blanky == topRow:
                    if blankx in (1, 2, 3):
                        return LEFT
                    elif blankx == 0:
                        return DOWN
                elif blanky == bottomRow:
                    if blankx in (1, 2):
                        return RIGHT
                    elif blankx == 3:
                        return UP
            elif notDone_x == 1:
                # move CCW
                if blanky == topRow:
                    if blankx in (1, 2, 3):
                        return LEFT
                    elif blankx == 0:
                        return DOWN
                elif blanky == bottomRow:
                    if blankx in (0, 2):
                        return RIGHT
                    elif blankx == 3:
                        return UP
            elif notDone_x == 2:
                # move CCW to bring notDone into topRow, col-1
                if blanky == topRow:
                    if blankx in (1, 2, 3):
                        return LEFT
                    elif blankx == 0:
                        return DOWN
                elif blanky == bottomRow:
                    if blankx in (0, 1):
                        return RIGHT
                    elif blankx == 3:
                        return UP
            elif notDone_x == 3:
                # move CW to bring notDone into topRow swap columns
                if blanky == topRow:
                    if blankx in (0, 1, 2):
                        return RIGHT
                    elif blankx == 3:
                        return DOWN
                elif blanky == bottomRow:
                    if blankx == 0:
                        return UP
                    elif blankx in (1, 2):
                        return LEFT  
    # notDone betw Tc,Td:
    elif betwTcTd:
        if notDone_y == topRow:
            if notDone_x == 0:
                if blanky == topRow:
                    return LEFT
                elif blanky == bottomRow:
                    if blankx in (0, 1, 2):
                        return RIGHT
                    else:
                        return UP
            elif notDone_x == 1:
                if blanky == topRow:
                    if blankx in (2, 3):
                        return LEFT
                    elif blankx == 0:
                        return DOWN
                elif blanky == bottomRow:
                    if blankx in (0, 1, 2):
                        return RIGHT
                    else:
                        return UP
            elif notDone_x == 2:
                if blanky == topRow:
                    if blankx == 1:
                        return LEFT
                    elif blankx in (0, 3):
                        return DOWN
                elif blanky == bottomRow:
                    # no 2 in following tuple b/c when blankx==2, a cross-swap
                    # takes place
                    if blankx in (0, 1):
                        return RIGHT
                    elif blankx == 3:
                        return LEFT  # in position now to cross-swap
            elif notDone_x == 3:
                if blanky == topRow:
                    if blankx in (0, 1, 2):
                        return RIGHT
                elif blanky == bottomRow:
                    if blankx == 0:
                        return UP
                    elif blankx in (1, 2, 3):
                        return LEFT
        # notDone in bottomRow:
        elif notDone_y == bottomRow:
            if notDone_x == 0:
                if blanky == topRow:
                    if blankx in (1, 2, 3):
                        return LEFT
                    elif blankx == 0:
                        return DOWN
                elif blanky == bottomRow:
                    if blankx in (1, 2):
                        return RIGHT
                    elif blankx == 3:
                        return UP
            elif notDone_x == 1:
                if blanky == topRow:
                    if blankx in (1, 2, 3):
                        return LEFT
                    elif blankx == 0:
                        return DOWN
                elif blanky == bottomRow:
                    if blankx in (0, 2):
                        return RIGHT
                    elif blankx == 3:
                        return UP
            elif notDone_x == 2:
                if blanky == topRow:
                    if blankx in (0, 1, 2):
                        return RIGHT
                    elif blankx == 3:
                        return DOWN
                elif blanky == bottomRow:
                    if blankx in (1, 3):
                        return LEFT
                    elif blankx == 0:
                        return UP
            elif notDone_x == 3:
                if blanky == topRow:
                    if blankx in (0, 1, 2):
                        return RIGHT
                    elif blankx == 3:
                        return DOWN
                elif blanky == bottomRow:
                    if blankx in (1, 2):
                        return LEFT
                    elif blankx == 0:
                        return UP


def moveTwoNotDone(Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx, Tdy, blankx, blanky,
                   notDone1_x, notDone1_y, notDone2_x, notDone2_y, topRow,
                   bottomRow):
    """Returns nextMove (one of UP, DOWN, RIGHT, LEFT) for the case when there
    are two of Q,R,S (see makeAdjacent4) to be moved betw Ta,Td.  This ftn is
    called from makeAdjacent4.  Again, the context here is 2 rows by 4 columns,
    with Ta-Td in the correct order for rotation into their final places."""
    # Here we do not need to worry whether the notDone tile in a cross-swap
    # position is in the topRow or the bottomRow, since this will not be the
    # last swap.

    # First see if we can make a swap.
    if (blanky == topRow and blankx == 1 and Tay == topRow and Tax > blankx and
        Tdx == 0):
        if notDone1_y == bottomRow and notDone1_x == blankx:
            return DOWN
        elif notDone2_y == bottomRow and notDone2_x == blankx:
            return DOWN
    elif (blanky == topRow and blankx == 2 and Tax > blankx and Tdx < blankx):
        if notDone1_y == bottomRow and notDone1_x == blankx:
            return DOWN
        elif notDone2_y == bottomRow and notDone2_x == blankx:
            return DOWN
    # blank in bottomRow:
    elif (blanky == bottomRow and blankx == 1 and Tax < blankx and
          Tdy == bottomRow and Tdx > blankx):
        if notDone1_y == topRow and notDone1_x == blankx:
            return UP
        elif notDone2_y == topRow and notDone2_x == blankx:
            return UP
    elif (blanky == bottomRow and blankx == 2 and Tay == bottomRow and
          Tax < blankx and Tdx > blankx):
        if notDone1_y == topRow and notDone1_x == blankx:
            return UP
        elif notDone2_y == topRow and notDone2_x == blankx:
            return UP

    # In order for a cross-swap to happen, we need Ta,Td apart.  In the logic
    # that follows, I try to move blank in the direction that allows for the
    # quickest cross-swap.
    if Tay == topRow:
        if Tax == 0:
            if blanky == bottomRow:
                if blankx == 0:
                    if ((notDone1_y == topRow and notDone1_x == 1) or
                        (notDone2_y == topRow and notDone2_x == 1)):
                        return RIGHT  # allows for quick swap
                    else:
                        return UP
                elif blankx in (1, 2, 3):
                    return LEFT
            elif blanky == topRow:
                if blankx == 3:
                    return DOWN  # move CW to pull Td further from Ta
                else:
                    return RIGHT  # move CW to pull Td further from Ta
        elif Tax == 1:
            if blanky == bottomRow:
                if blankx in (0, 3):
                    return UP
                elif blankx in (1, 2):
                    return RIGHT
            elif blanky == topRow:
                if blankx == 0:
                    return RIGHT
                elif blankx in (2, 3):
                    return LEFT
        elif Tax == 2:
            if blanky == bottomRow:  # forces Td into topRow with Tdx == 0
                if blankx == 0:
                    if ((notDone1_y == bottomRow and notDone1_x == 1) or
                        (notDone2_y == bottomRow and notDone2_x == 1)):
                        return UP  # move CW to swap on next move
                    else:
                        return RIGHT  # move CCW for much quicker swap
                elif blankx == 1:
                    if ((notDone1_y == bottomRow and notDone1_x == 0) or
                        (notDone2_y == bottomRow and notDone2_x == 0)):
                        return LEFT  # move CW to swap after next couple moves
                    else:
                        return RIGHT  # move CCW for much quicker swap
                elif blankx == 2:
                    return RIGHT
                elif blankx == 3:
                    return UP
            elif blanky == topRow:
                if blankx == 0:
                    if ((notDone1_y == bottomRow and notDone1_x == 1) or
                        (notDone2_y == bottomRow and notDone2_x == 1)):
                        return RIGHT  # swap on next move
                    else:
                        return DOWN
                elif blankx in (1, 3):
                    return LEFT                   
        elif Tax == 3:
            if blanky == bottomRow:
                if blankx == 0:
                    return UP  # move CW to pull Td away from Ta
                elif blankx == 1:
                    return LEFT  # move CW to pull Td away from Ta
                elif blankx == 2:
                    if ((notDone1_y == bottomRow and notDone1_x == 3) or
                        (notDone2_y == bottomRow and notDone2_x == 3)):
                        return RIGHT  # allows for quick swap
                    else:
                        return LEFT  # move CW to pull Td away from Ta
                elif blankx == 3:
                    if ((notDone1_y == bottomRow and notDone1_x == 2) or
                        (notDone2_y == bottomRow and notDone2_x == 2)):
                        return UP  # for quick swap 
                    else:
                        return LEFT  # move CW to pull Td away from Ta
            elif blanky == topRow:
                if blankx == 0:
                    if ((notDone1_y == bottomRow and notDone1_x in (1, 2)) or
                        (notDone2_y == bottomRow and notDone2_x in (1, 2))):
                        return RIGHT
                    else:
                        return DOWN
                elif blankx == 1:
                    if ((notDone1_y == bottomRow and notDone1_x == 2) or
                        (notDone2_y == bottomRow and notDone2_x == 2)):
                        return RIGHT
                    else:
                        return LEFT
                elif blankx == 2:
                    return LEFT
    # Ta in bottomRow:
    elif Tay == bottomRow:
        if Tax == 0:
            if blanky == bottomRow:
                if blankx == 1:
                    return RIGHT
                elif blankx == 2:
                    if ((notDone1_y == topRow and notDone1_x == 1) or
                        (notDone2_y == topRow and notDone2_x == 1)):
                        return LEFT
                    else:
                        return RIGHT
                elif blankx == 3:
                    return LEFT  # move CW to pull Td away from Ta
            elif blanky == topRow:
                if blankx in (0, 1, 2):
                    return RIGHT  # move CW to pull Td away from Ta
                else:
                    return DOWN
        elif Tax == 1:
            if blanky == bottomRow:
                if blankx in (0, 2):
                    return RIGHT  # move CCW for separating Ta,Td
                elif blankx == 3:
                    if ((notDone1_y == topRow and notDone1_x == 2) or
                        (notDone2_y == topRow and notDone2_x == 2)):
                        return LEFT
                    else:
                        return UP
            elif blanky == topRow:  # forces Td into bottomRow, Tdx == 3
                if blankx == 0:
                    if ((notDone1_y == topRow and notDone1_x == 3) or
                        (notDone2_y == topRow and notDone2_x == 3)):
                        return RIGHT
                    else:
                        return DOWN
                elif blankx == 1:
                    if ((notDone1_y == topRow and notDone1_x == 3) or
                        (notDone2_y == topRow and notDone2_x == 3)):
                        return RIGHT
                    else:
                        return LEFT
                elif blankx == 2:
                    if ((notDone1_y == topRow and notDone1_x == 3) or
                        (notDone2_y == topRow and notDone2_x == 3)):
                        return RIGHT
                    else:
                        return LEFT
                elif blankx == 3:
                    if ((notDone1_y == topRow and notDone1_x == 2) or
                        (notDone2_y == topRow and notDone2_x == 2)):
                        return DOWN
                    else:
                        return LEFT
        elif Tax == 2:
            if blanky == bottomRow:
                if blankx in (0, 1):
                    return RIGHT  # pull Ta apart from Td
                elif blankx == 3:
                    return UP
            elif blanky == topRow:  # forces Td into topRow, Tdx == 3
                if blankx == 0:
                    return DOWN
                else:
                    return LEFT
        elif Tax == 3:
            if blanky == bottomRow:
                if blankx == 0:
                    if ((notDone1_y == bottomRow and notDone1_x == 2) or
                        (notDone2_y == bottomRow and notDone2_x == 2)):
                        return UP
                    else:
                        return RIGHT
                elif blankx == 1:
                    if ((notDone1_y == bottomRow and notDone1_x == 2) or
                        (notDone2_y == bottomRow and notDone2_x == 2)):
                        return LEFT
                    else:
                        return RIGHT
                elif blankx == 2:
                    return RIGHT
            elif blanky == topRow:
                if blankx in (0, 1, 2):
                    return RIGHT
                elif blankx == 3:
                    if ((notDone1_y == bottomRow and notDone1_x == 2) or
                        (notDone2_y == bottomRow and notDone2_x == 2)):
                        return LEFT
                    else:
                        return DOWN


def moveThreeNotDone(Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx, Tdy, blankx, blanky,
                     Qx, Qy, Rx, Ry, Sx, Sy, topRow, bottomRow):
    """Returns nextMove (one of UP, DOWN, LEFT, RIGHT) for the case when all of
    Q,R,S need to be moved betw. Ta and Td.  This ftn is called from 
    makeAdjacent4.  Again, the context here is 2 rows by 4 columns, with
    Ta-Td in the correct order for rotation into their final places."""
    
    # First see if we can make a swap.
    if (blanky == topRow and blankx in (1, 2) and Tay == topRow and 
        Tax > blankx and Tdy == topRow and Tdx < blankx):
        if Qy == bottomRow and Qx == blankx:
            return DOWN
        elif Ry == bottomRow and Rx == blankx:
            return DOWN
        elif Sy == bottomRow and Sx == blankx:
            return DOWN
    elif (blanky == bottomRow and blankx in (1, 2) and Tay == bottomRow and
          Tax < blankx and Tdy == bottomRow and Tdx > blankx):
        if Qy == topRow and Qx == blankx:
            return UP
        elif Ry == topRow and Rx == blankx:
            return UP
        elif Sy == topRow and Sx == blankx:
            return UP
       
    # Special logic is required when one of Q,R,S is in each of the gaps, i.e.,
    # when TaTb_cont, TbTc_cont, and TcTd_cont are all false.  When this
    # scenario occurs, we can rotate blank through the tiles and never have
    # the above cross-swap conditions met.
    TaTb_cont = False
    if adjacent2(Tax, Tay, Tbx, Tby, blankx, blanky):
        TaTb_cont = True
    TbTc_cont = False
    if adjacent2(Tbx, Tby, Tcx, Tcy, blankx, blanky):
        TbTc_cont = True
    TcTd_cont = False
    if adjacent2(Tcx, Tcy, Tdx, Tdy, blankx, blanky):
        TcTd_cont = True
    
    if TaTb_cont == False and TbTc_cont == False and TcTd_cont == False:
        nextMove = move3NotDoneSpecial(Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx, Tdy,
                                       blankx, blanky, Qx, Qy, Rx, Ry, Sx, Sy,
                                       topRow, bottomRow)
        return nextMove
    
    # Goal: reduce the scenario to one of twoNotDone.             
    if Tay == topRow:
        if Tax == 0:
            if blanky == topRow:
                # Td will be directly below Ta
                return LEFT
            elif blanky == bottomRow:
                if blankx == 0:
                    return UP
                elif blankx in (1, 2, 3):
                    return LEFT
        elif Tax == 1:
            if blanky == topRow:
                if blankx == 0:
                    return DOWN  # moves Td into upper left corner
                elif blankx in (2, 3):
                    return LEFT
            elif blanky == bottomRow:
                if blankx in (0, 1, 2):
                    return RIGHT
                else:
                    return UP
        elif Tax == 2:
            if blanky == topRow:
                if blankx == 0:
                    if anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, bottomRow)):
                        return RIGHT
                    else:
                        return DOWN
                elif blankx == 1:
                    return LEFT
                elif blankx == 3:
                    if(anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (0, bottomRow))
                       and not anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy,
                                            (2, bottomRow))):
                        return DOWN
                    else:
                        return LEFT
            elif blanky == bottomRow:
                if blankx == 0:  # keep default direction the same
                    if anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, bottomRow)):
                        return UP
                    else:
                        return RIGHT
                elif blankx == 1:
                    if anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (0, bottomRow)):
                        return LEFT
                    else:
                        return RIGHT
                elif blankx == 2:
                    if (anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (0, bottomRow)) and
                        not anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (3, bottomRow))):
                        return LEFT
                    else:
                        return RIGHT
                elif blankx == 3:
                    if (anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (0, bottomRow)) and
                        not anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, bottomRow))):
                        return LEFT
                    else:
                        return UP
        elif Tax == 3:
            if blanky == topRow:
                if blankx in (0, 1, 2):
                    return RIGHT
            elif blanky == bottomRow:
                if blankx == 0:
                    return UP
                elif blankx in (1, 2, 3):
                    return LEFT
    # Ta is in bottomRow:
    elif Tay == bottomRow:
        if Tax == 0:
            if blanky == topRow:
                if blankx in (0, 1, 2):
                    return RIGHT
                elif blankx == 3:
                    return DOWN
            elif blanky == bottomRow:
                if blankx in (1, 2, 3):
                    return LEFT
        elif Tax == 1:
            if blanky == topRow:
                if blankx == 0:
                    if anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, topRow)):
                        return DOWN
                    else:
                        return RIGHT
                elif blankx == 1:
                    if anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (0, topRow)):
                        return LEFT
                    else:
                        return RIGHT
                elif blankx == 2:
                    if (anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (0, topRow)) and
                        not anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (3, topRow))):
                        return LEFT
                    else:
                        return RIGHT
                elif blankx == 3:
                    if (anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (0, topRow)) and
                        not anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, topRow))):
                        return LEFT
                    else:
                        return DOWN
            elif blanky == bottomRow:
                if blankx == 0:
                    if anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, topRow)):
                        return RIGHT
                    else:
                        return UP
                elif blankx == 2:
                    if anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (0, topRow)):
                        return RIGHT
                    else:
                        return LEFT
                elif blankx == 3:
                    if anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, topRow)):
                        return LEFT
                    else:
                        return UP
        elif Tax == 2:
            if blanky == topRow:
                if blankx == 0:
                    return DOWN
                elif blankx in (1, 2, 3):
                    return LEFT
            elif blanky == bottomRow:
                if blankx in (0, 1):
                    return RIGHT
                elif blankx == 3:
                    return UP
        elif Tax == 3:
            if blanky == topRow:
                if blankx == 0:
                    if anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, bottomRow)):
                        return RIGHT
                    else:
                        return DOWN
                elif blankx == 1:
                    if anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, bottomRow)):
                        return RIGHT
                    else:
                        return LEFT
                elif blankx == 2:
                    return RIGHT
                elif blankx == 3:
                    return DOWN
            elif blanky == bottomRow:
                if blankx == 0:
                    if (not anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (0, topRow)) and
                        not anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, topRow))):
                        return UP
                    else:
                        return RIGHT
                elif blankx in (1, 2):
                    if (not anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (0, topRow)) and
                        not anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, topRow))):
                        return LEFT
                    else:
                        return RIGHT


def move3NotDoneSpecial(Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx, Tdy, blankx, blanky,
                        Qx, Qy, Rx, Ry, Sx, Sy, topRow, bottomRow):
    """Returns nextMove (one of UP, DOWN, LEFT, RIGHT) for a special case of 
    threeNotDone (see makeAdjacent4).  This ftn is called from
    moveThreeNotDone and from putLast3betw.  Ta - Td are in correct order for
    rotation into their final places.  This ftn is different from its siblings
    because of the cross-swap it allows.  Without this special cross-swap, we
    would end up in an infinite loop if one each of Q,R,S is in each of the
    gaps betw Ta-Tb, Tb-Tc, and Tc-Td.."""
    
    # When one of Q,R,S are in each of the gaps betw. Ta - Td (except the TdTa
    # gap), we need to do a special cross-swap to avoid entering an infinite
    # loop.
    
    # First see if we can make a swap.  This special swap brings an extra
    # one of Q,R,S either betw Ta and Tb, betw Tb and Tc, or betw Tc and Td.
    # The best locations are betw Ta,Tb or betw Tc,Td.
    if (blanky == topRow and blankx in (1, 2) and ((Tax < blankx and
        Tdx < blankx) or (Tax > blankx and Tdx > blankx))):
        if Qy == bottomRow and Qx == blankx:
            return DOWN
        elif Ry == bottomRow and Rx == blankx:
            return DOWN
        elif Sy == bottomRow and Sx == blankx:
            return DOWN
    elif (blanky == bottomRow and blankx in (1, 2) and ((Tax > blankx and
          Tdx > blankx) or (Tax < blankx and Tdx < blankx))):
        if Qy == topRow and Qx == blankx:
            return UP
        elif Ry == topRow and Rx == blankx:
            return UP
        elif Sy == topRow and Sx == blankx:
            return UP

    # Ta in topRow:
    if Tay == topRow:
        if Tax == 0:  # forces Td to be in lower left corner
            if blanky == topRow and blankx in (2, 3):
                return LEFT  # if blankx == 1, we can cross-swap
            elif blanky == bottomRow:
                if blankx in (2, 3):
                    return LEFT
                elif blankx == 0:
                    return RIGHT  # if blankx == 1, we can cross-swap
        elif Tax == 1:
            if blanky == topRow:
                if blankx == 0:
                    return RIGHT  # if blankx == 1, we can cross-swap
                elif blankx == 3:
                    return LEFT  # if blankx == 2, we can cross-swap
            elif blanky == bottomRow:
                if blankx in (0, 1):
                    return RIGHT  # if blankx== 2, we can cross-swap into Tb,Tc
                elif blankx == 3:
                    return LEFT
        elif Tax == 2:
            if blanky == topRow:
                if blankx in (0, 1):
                    return RIGHT  # if blankx == 2, we can cross-swap
                elif blankx == 3:
                    return LEFT  # if blankx == 1, we can cross-swap into Tc,Td
            elif blanky == bottomRow:
                if blankx in (0, 3):
                    return UP
                elif blankx == 1:
                    return LEFT
                elif blankx == 2:
                    return RIGHT
        elif Tax == 3:
            if blanky == topRow:
                if blankx == 0:  # if blankx == 1, we can cross-swap
                    return RIGHT
                elif blankx == 2:
                    return LEFT
            elif blanky == bottomRow:
                if blankx in (0, 3):
                    return UP  # if blankx == 1, we can cross-swap
                elif blankx == 2:
                    return LEFT
    # Ta in bottomRow:
    elif Tay == bottomRow:
        if Tax == 0:
            if blanky == topRow:
                if blankx == 0:
                    return DOWN
                elif blankx == 1:
                    return RIGHT
                elif blankx == 3:  # if blankx == 2, we can cross-swap into
                    return LEFT    # Tb, Tc
            elif blanky == bottomRow:
                if blankx == 1:  # if blankX == 2, we can cross-swap
                    return RIGHT
                elif blankx == 3:
                    return LEFT
        elif Tax == 1:
            if blanky == topRow:
                if blankx in (0, 3):
                    return DOWN
                elif blankx == 1:
                    return LEFT
                elif blankx == 2:
                    return RIGHT
            elif blanky == bottomRow:
                if blankx == 0:
                    return RIGHT
                elif blankx in (2, 3):
                    return LEFT
        elif Tax == 2:
            if blanky == topRow:
                if blankx == 0:  # if blankx == 1, we can cross-swap into Tb,Tc
                    return RIGHT
                elif blankx in (2, 3):
                    return LEFT
            elif blanky == bottomRow:  # if blankx == 1, we can cross-swap
                if blankx == 0:
                    return RIGHT
                elif blankx == 3:
                    return LEFT  # if blankx == 2, we can cross-swap into Ta,Td
        elif Tax == 3:
            if blanky == topRow:
                if blankx in (0, 1):  # if blankx == 2, we can cross-swap
                    return RIGHT
                elif blankx == 3:
                    return LEFT
            elif blanky == bottomRow:
                if blankx in (0, 1):  # if blankx == 2, we can cross-swap
                    return RIGHT


#############################################################################
###
#############################################################################
