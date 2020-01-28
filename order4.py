# -*- coding: utf-8 -*-
"""
@author: Greg Schaefer

module name: order4.py

module contents (10 ftns):

    - adjacent3
    - QRSbetw
    - inOrder
    - reversedTiles
    - getTrueReversedTs
    - putTileBetw
    - continueDirCCW
    - putTbetwSpec
    - fixReversal
    - order4
    

Released under a GNU GPLv3 license. 

"""

#############################################################################
### order4.py COPYRIGHT:
#############################################################################

# SlidePuzzlePlus, order4.py
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
### order4.py
#############################################################################

from constants_and_genFtns import *
from makeAdjacent4 import *

#############################################################################
### helper ftns for order4
#############################################################################


def adjacent3(Tax, Tay, Tbx, Tby, Tcx, Tcy, blankx, blanky):
    """Returns True if all of Ta, Tb, and Tc are contiguous, blank excepted,
    or if Ta, Tc, Tb are contiguous.  (This ftn could be changed to return
    True for all 6 permutations, but the way it is currently used, the
    present logic will do."""
    returnVal = False
    if (adjacent2(Tax, Tay, Tbx, Tby, blankx, blanky) and
        adjacent2(Tbx, Tby, Tcx, Tcy, blankx, blanky)):
        returnVal = True
    elif (adjacent2(Tax, Tay, Tcx, Tcy, blankx, blanky) and
          adjacent2(Tcx, Tcy, Tbx, Tby, blankx, blanky)):
        returnVal = True
    return returnVal


def QRSbetw(T1x, T1y, T2x, T2y, Qx, Qy, Rx, Ry, Sx, Sy, blankx, blanky,
            topRow, bottomRow):
    """Returns True if exactly one of Q,R,S is between T1 and T2."""    
    if tileBetw(T1x, T1y, T2x, T2y, Qx, Qy, blankx, blanky, topRow, bottomRow):
        return True
    elif tileBetw(T1x, T1y, T2x, T2y, Rx, Ry, blankx, blanky, topRow, bottomRow):
        return True
    elif tileBetw(T1x, T1y, T2x, T2y, Sx, Sy, blankx, blanky, topRow, bottomRow):
        return True
    else:
        return False


def inOrder(Tax, Tay, Tbx, Tby, Tcx, Tcy, topRow, bottomRow):
    """Returns True if the three tiles are in the order required for rotation
    into their final positions.  Context is the 2 rows by 4 columns framework.
    Because at this point the tiles needn't be contiguous, it is possible to
    have Ta to the far right of Tb in the topRow and still have these tiles in
    order (topRow might look like: Tb, Tc, Td, Ta).  Thus, to determine
    whether the order betw two tiles is correct, we always have to use at least
    3 tiles."""

    # Example: If we check the order of Tc-Td-Ta, Tc would be denoted by 'Ta',
    # Td by 'Tb', and Ta by 'Tc'.
    returnVal = False
    # Case 1: Ta,Tb, Tc are all in the topRow
    if Tay == topRow and Tby == topRow and Tcy == topRow:
        if (Tax < Tbx and Tbx < Tcx) or (Tbx < Tcx and Tcx < Tax) or (Tcx < Tax and Tax < Tbx):
            returnVal = True
    # Case 2: Ta,Tb, Tc are all in the bottomRow
    elif Tay == bottomRow and Tby == bottomRow and Tcy == bottomRow:
        if (Tcx < Tbx and Tbx < Tax) or (Tax < Tcx and Tcx < Tbx) or (Tbx < Tax and Tax < Tcx):
            returnVal = True
    # Case 3: Tb,Tc in topRow; Ta in bottomRow
    elif Tby == topRow and Tcy == topRow and Tay == bottomRow:
        if Tbx < Tcx:
            returnVal = True
    # Case 4: Tc,Ta in topRow; Tb in bottomRow
    elif Tcy == topRow and Tay == topRow and Tby == bottomRow:
        if Tcx < Tax:
            returnVal = True
    # Case 5: Ta,Tb in topRow; Tc in bottomRow
    elif Tay == topRow and Tby == topRow and Tcy == bottomRow:
        if Tax < Tbx:
            returnVal = True
    # Case 6: Tb,Tc in bottomRow; Ta in topRow
    elif Tby == bottomRow and Tcy == bottomRow and Tay == topRow:
        if Tcx < Tbx:
            returnVal = True
    # Case 7: Tc,Ta in bottomRow; Tb in topRow
    elif Tcy == bottomRow and Tay == bottomRow and Tby == topRow:
        if Tax < Tcx:
            returnVal = True
    # Case 8: Ta,Tb in bottomRow; Tc in topRow
    elif Tay == bottomRow and Tby == bottomRow and Tcy == topRow:
        if Tbx < Tax:
            returnVal = True
    return returnVal


def reversedTiles(H, L, Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx, Tdy, blankx, blanky, 
                  topRow, bottomRow, Qx, Qy, Rx, Ry, Sx, Sy):
    """Returns True if H and L are reversed in terms of the order needed for
    the tiles to be rotated into their final positions.  This ftn is very much
    like inOrder, but is better in that it directly tells us, for any two
    tiles tested, whether the tiles are reversed in order.  What it does not do
    is tell us the quickest way to fix one or both reversals (there can be at
    most two necessary fixes)."""
    
    returnVal = False
    walkPath = [(0, topRow), (1, topRow), (2, topRow), (3, topRow),
                (3, bottomRow), (2, bottomRow), (1, bottomRow), (0, bottomRow)]
    tileDict = {'Ta': (Tax, Tay), 'Tb': (Tbx, Tby), 'Tc': (Tcx, Tcy),
                'Td': (Tdx, Tdy), 'blank': (blankx, blanky), 'Q': (Qx, Qy),
                'R': (Rx, Ry), 'S': (Sx, Sy), (Tax, Tay): 'Ta', (Tbx, Tby): 'Tb',
                (Tcx, Tcy): 'Tc', (Tdx, Tdy): 'Td', (blankx, blanky): 'blank',
                (Qx, Qy): 'Q', (Rx, Ry): 'R', (Sx, Sy): 'S'}
    walkPathDict = {(0, topRow): 1, (1, topRow): 2, (2, topRow): 3,
                    (3, topRow): 4, (3, bottomRow): 5, (2, bottomRow): 6,
                    (1, bottomRow): 7, (0, bottomRow): 8, 1: (0, topRow),
                    2: (1, topRow), 3: (2, topRow), 4: (3, topRow),
                    5: (3, bottomRow), 6: (2, bottomRow), 7: (1, bottomRow),
                    8: (0, bottomRow)}
        
    # H = tile with higher value; L = tile with lower value; the values for
    # H and L will be one of the strings, 'Ta', 'Tb', 'Tc', or 'Td'
    # startpt holds the coordinates of the tile from which the search is
    # started
    startpt = tileDict[H]
    # endpt will be the tile coordinates at which the search stops
    if H != 'Td':
        endpt_name = 'Td'
    elif H == 'Td' and L == 'Ta':
        endpt_name = 'Td'  # forcing while loop to NOT execute
    elif H == 'Td' and L == 'Tb':
        endpt_name = 'Ta'  # if we see Tb before Ta, we can say Td,Tb are reversed
    elif H == 'Td' and L == 'Tc':
        endpt_name = 'Tb'  # if we see Tc before Tb, we can say Td,Tc are reversed
        
    endpt = tileDict[endpt_name]
    
    # To identify whether two tiles have a reverse order, we can search in a
    # clockwise (CW) direction through the 2 rows by 4 columns structure, from
    # startpt to endpt.  If we encounter tile L prior to reaching the endpt,
    # we know that H and L are in reverse order.  (Note that we can never have
    # L equal to 'Td'.)
    # We need to walk through walkPath, the index of which ranges from 0 to 7.
    startpt_index = walkPathDict[startpt] - 1
    curTile = H
    i = 1
    while i < 8 and curTile != endpt_name:
        walkPath_index = (startpt_index + i) % 8
        curCoords = walkPath[walkPath_index]
        curTile = tileDict[curCoords]
        if curTile == L:
            returnVal = True
            break
        i += 1

    # Ta can be on either side of Td except if it upsets order betw. Td,Tc.       
    if H == 'Td' and L == 'Ta':
        returnVal = False
        test1 = reversedTiles('Tc', 'Ta', Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx, Tdy,
                              blankx, blanky, topRow, bottomRow, Qx, Qy, Rx, Ry,
                              Sx, Sy)
        test2 = reversedTiles('Tb', 'Ta', Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx, Tdy,
                              blankx, blanky, topRow, bottomRow, Qx, Qy, Rx, Ry,
                              Sx, Sy)
        test3 = reversedTiles('Tc', 'Tb', Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx, Tdy,
                              blankx, blanky, topRow, bottomRow, Qx, Qy, Rx, Ry, Sx, Sy)
        # test4 needed due to Unit Test 28.
        test4 = reversedTiles('Td', 'Tc', Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx, Tdy,
                              blankx, blanky, topRow, bottomRow, Qx, Qy, Rx, Ry, Sx, Sy)
        
        if test1 and not (test2 and test3) and not test4:
            returnVal = True      
    return returnVal


def getTrueReversedTs(Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx, Tdy, blankx, blanky,
                      Qx, Qy, Rx, Ry, Sx, Sy, topRow, bottomRow):
    """Returns a list of tuples of the tile names that are truly reversed.  The
    list returned should never be more than 2 tuples in length."""
    
    # Identify the tile or tiles out of order.  Because we are working with
    # two rows over which we can rotate the tiles, we can have at most two
    # reversals.  E.g., if order on bottom row is, from left to right, Ta, Tb,
    # Tc, Td, we only need to reverse Td with Tc and Tb with Ta to have an 
    # ordering of the tiles that is ready for rotation.  Similarly, if we have
    # not TaTbTc_done, the fix is to reverse either Tb with Ta or Tc with Tb.
    # The tile in the middle always needs to be moved for the fix.
    
    TbTa_reversed = reversedTiles('Tb', 'Ta', Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx,
                                  Tdy, blankx, blanky, topRow,bottomRow,
                                  Qx, Qy, Rx, Ry, Sx, Sy)
    TcTb_reversed = reversedTiles('Tc', 'Tb', Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx,
                                  Tdy, blankx, blanky, topRow,bottomRow,
                                  Qx, Qy, Rx, Ry, Sx, Sy)
    TdTc_reversed = reversedTiles('Td', 'Tc', Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx,
                                  Tdy, blankx, blanky, topRow,bottomRow,
                                  Qx, Qy, Rx, Ry, Sx, Sy)
    TdTa_reversed = reversedTiles('Td', 'Ta', Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx,
                                  Tdy, blankx, blanky, topRow,bottomRow,
                                  Qx, Qy, Rx, Ry, Sx, Sy)
    TcTa_reversed = reversedTiles('Tc', 'Ta', Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx,
                                  Tdy, blankx, blanky, topRow,bottomRow,
                                  Qx, Qy, Rx, Ry, Sx, Sy)
    TdTb_reversed = reversedTiles('Td', 'Tb', Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx,
                                  Tdy, blankx, blanky, topRow,bottomRow,
                                  Qx, Qy, Rx, Ry, Sx, Sy)
    
    # the following four checks are probably unnecessary           
    if TbTa_reversed and inOrder(Tax, Tay, Tbx, Tby, Tcx, Tcy, topRow, bottomRow):
        TbTa_reversed = False

    if TcTb_reversed and inOrder(Tbx, Tby, Tcx, Tcy, Tdx, Tdy, topRow, bottomRow):
        TcTb_reversed = False

    if TdTc_reversed and inOrder(Tcx, Tcy, Tdx, Tdy, Tax, Tay, topRow, bottomRow):
        TdTc_reversed = False

    if TdTa_reversed and inOrder(Tdx, Tdy, Tax, Tay, Tbx, Tby, topRow, bottomRow):
        TdTa_reversed = False
        
    # TcTa and TdTb are different from the above checks due to the distance
    # betw the tiles 
        
    # The following filters are based on the unit tests.
    if TdTa_reversed and inOrder(Tax, Tay, Tbx, Tby, Tcx, Tcy, topRow, bottomRow):
        TcTa_reversed = False
        TdTb_reversed = False
    if TbTa_reversed and inOrder(Tdx, Tdy, Tbx, Tby, Tcx, Tcy, topRow, bottomRow):
        TdTb_reversed = False
    if TdTc_reversed and inOrder(Tax, Tay, Tbx, Tby, Tcx, Tcy, topRow, bottomRow):
        TcTb_reversed = False
        if inOrder(Tdx, Tdy, Tax, Tay, Tbx, Tby, topRow, bottomRow):
            TcTa_reversed = False  # see UnitTest 10 for this ftn
            
    # The logic in order4 is made simpler if we never return the TcTa and TdTb
    # reversals.  Both of these reversals are equivalent to double reversals.
    # A TcTa reversal is equivalent to having both TdTa and TcTb reversed, or
    # both TbTa and TdTc reversed.  A TdTb reversal is also equivalent to the
    # same: TdTa + TcTb, which is equal to TbTa + TdTc.
    if TcTa_reversed:
        #TdTa_reversed = True
        TdTc_reversed = True
        TbTa_reversed = True
        TcTa_reversed = False
    if TdTb_reversed:
        #TbTa_reversed = True
        TdTc_reversed = True
        TbTa_reversed = True
        TdTb_reversed = False

    returnList = []
    # tile with smaller value comes first in the tuple except when we have a
    # TdTa reversal.
    if TbTa_reversed:
        returnList.append(('Ta', 'Tb'))
    if TcTb_reversed:
        returnList.append(('Tb', 'Tc'))
    if TdTc_reversed:
        returnList.append(('Tc', 'Td'))
    # Note that 'Ta' acts as the "high tile", or highT, in a TdTa reversal.
    if TdTa_reversed:
        returnList.append(('Td', 'Ta'))
    if TcTa_reversed:
        returnList.append(('Ta', 'Tc'))
    if TdTb_reversed:
        returnList.append(('Tb', 'Td'))
        
    if len(returnList) >= 3:
        returnList = [('Ta', 'Tb'), ('Tc', 'Td')]
        
    return returnList


def putTileBetw(highTx, highTy, lowTx, lowTy, blankx, blanky, Qx, Qy, Rx, Ry,
                Sx, Sy, topRow, bottomRow):
    """Returns nextMove (one of UP, DOWN, LEFT, RIGHT) for scenario when one of
    Q,R,S needs to be inserted betw the high and low tiles in the 2 rows by 4
    columns context.  This ftn is called from order4, whose task is to order
    the 4 tiles of a row so that they can be rotated into their final
    positions.  When this ftn is called, highT and lowT are reversed.
    It is not always the case that one of Q,R,S has to be betw highT and lowT
    in order to get Ta - Td in order.  If the non-reversed tiles are close
    together (generally not more than one non-blank tile apart), they can be
    separated from the reversed tiles enough for the necessary cross-swap to
    take place.  When this ftn is called, we will always have at least 2 of
    Q,R,S betw n1 and n2, the non-reversed tiles.  The logic in this ftn does
    not require n1 and n2 to be in order; in fact, there is no reference to
    tiles n1 and n2 in this ftn.  The conditions under which this ftn is called
    are such that this ftn will never create the conditions under which
    putTbetwSpec needs to be called."""

    # Necessary conditions for a cross-swap: need to have one of Q,R,S in a
    # swap column, with blank below (or above) and betw the high and low tiles.

    # First see if we can swap with one of Q,R,S.  (No need here for special
    # logic to handle the TdTa reversal.  If we have a TdTa reversal, we will
    # have highT = Ta and lowT = Td.)
    if (blanky == topRow and blankx in (1, 2) and highTx == blankx - 1 and
        lowTx == blankx + 1):
        if Qy == bottomRow and Qx == blankx:
            return DOWN
        elif Ry == bottomRow and Rx == blankx:
            return DOWN
        elif Sy == bottomRow and Sx == blankx:
            return DOWN    
    elif (blanky == bottomRow and blankx in (1, 2) and highTx == blankx + 1 and
          lowTx == blankx - 1):
        if Qy == topRow and Qx == blankx:
            return UP
        elif Ry == topRow and Rx == blankx:
            return UP
        elif Sy == topRow and Sx == blankx:
            return UP

    # A TdTa_reversal is different from the other reversals in that the low
    # tile in this case (Ta) will precede the high tile (Td) when both are in
    # the topRow, even though the tiles are reversed.  This is just the opposite
    # of what we see with the other reversals.  Thus, the high-low mapping for
    # a TdTa reversal needs to be reversed, or inverted, in order for the
    # following logic to also apply to a TdTa reversal.  [This reversal is now
    # done in getTrueReversedTs().]
#    if (lowTx, lowTy) == (Tax, Tay) and (highTx, highTy) == (Tdx, Tdy):
#        lowTx, lowTy = Tdx, Tdy
#        highTx, highTy = Tax, Tay
    # (The above interchange works for the logic that follows because comparisons
    # to val(n2T) and val(n1T) are never made.)

    # Need high and/or low in a swap column so that when blank is betw, and in
    # a swap column, one of Q,R,S can be brought betw high and low.
    # REMINDER: when this ftn is called, we will always have at least 2 of
    # Q,R,S between n1 and n2, the non-reversed tiles.
    if blanky == topRow:
        if blankx == 0:
            if (((highTx, highTy) == (2, topRow) and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, bottomRow))) or
                ((highTx, highTy) == (1, topRow) and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, bottomRow)))):
                return RIGHT
            else:
                return DOWN  # default dir = CCW
        elif blankx == 1:
            # we always have at least two of Q,R,S betw n1 and n2
            if (((highTx, highTy) == (2, topRow) and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, bottomRow))) or
                ((highTx, highTy) == (2, bottomRow) and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (3, topRow)))):
                return RIGHT
            else:
                return LEFT  # default dir = CCW
        elif blankx == 2:
            if (((highTx, highTy) == (2, bottomRow) and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (3, topRow))) or
                ((highTx, highTy) == (1, bottomRow) and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, topRow)))):
                return RIGHT
            else:
                return LEFT  # default dir = CCW
        elif blankx == 3:
            if (((highTx, highTy) == (1, bottomRow) and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, topRow))) or
                ((highTx, highTy) == (2, bottomRow) and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, topRow)))):
                return DOWN
            else:
                return LEFT  # default dir = CCW
    elif blanky == bottomRow:
        if blankx == 0:
            if (((highTx, highTy) == (2, topRow) and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, bottomRow))) or
                ((highTx, highTy) == (1, topRow) and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, bottomRow)))):
                return UP
            else:
                return RIGHT  # default dir = CCW
        elif blankx == 1:
            if (((highTx, highTy) == (2, topRow) and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, bottomRow))) or
                ((highTx, highTy) == (1, topRow) and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (0, bottomRow)))):
                return LEFT
            else:
                return RIGHT  # default dir = CCW
        elif blankx == 2:
            if (((highTx, highTy) == (1, topRow) and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (0, bottomRow))) or
                ((highTx, highTy) == (2, topRow) and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, bottomRow))) or
                ((highTx, highTy) == (1, bottomRow) and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, topRow)))):
                return LEFT
            else:
                return RIGHT  # default dir = CCW
        elif blankx == 3:
            if (((highTx, highTy) == (2, bottomRow) and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (2, topRow))) or
                ((highTx, highTy) == (1, bottomRow) and anyQRSinCell(Qx, Qy, Rx, Ry, Sx, Sy, (1, topRow)))):
                return LEFT
            else:
                return UP  # default dir = CCW


def continueDirCCW(blankx, blanky, topRow, bottomRow):
    """Context is 2 rows by 4 columns.  Returns the next move for blank,
    continuing in a counter-clockwise direction."""
    if blanky == topRow:
        if blankx == 0:
            return DOWN
        elif blankx in (1, 2, 3):
            return LEFT
    elif blanky == bottomRow:
        if blankx in (0, 1, 2):
            return RIGHT
        elif blankx == 3:
            return UP


def putTbetwSpec(highTx, highTy, lowTx, lowTy, blankx, blanky, topRow,
                 bottomRow, Qx, Qy, Rx, Ry, Sx, Sy):
    """Returns nextMove (one of UP, DOWN, LEFT, RIGHT).  Need to have all 3
    of Q,R,S betw highT and lowT before we can call fixReversal.  When this ftn
    is called, n2High_adj and n1Low_adj are both true; also, there are
    exactly two of Q,R,S betw highT and lowT."""
    
    # Necessary conditions for a cross-swap: need to have one of Q,R,S in a
    # swap column, with blank below (or above) and betw the high and low tiles.

    # First see if we can swap with one of Q,R,S.  (No need here for special
    # logic to handle the TdTa reversal.)
    if (blanky == topRow and blankx == 2 and highTx == blankx - 2 and
        lowTx == blankx + 1 and highTy == bottomRow and lowTy == topRow):
        if Qy == bottomRow and Qx == blankx:
            return DOWN
        elif Ry == bottomRow and Rx == blankx:
            return DOWN
        elif Sy == bottomRow and Sx == blankx:
            return DOWN
    elif (blanky == bottomRow and blankx == 1 and highTx == blankx + 2 and
          lowTx == blankx - 1 and highTy == topRow and lowTy == bottomRow):
        if Qy == topRow and Qx == blankx:
            return UP
        elif Ry == topRow and Rx == blankx:
            return UP
        elif Sy == topRow and Sx == blankx:
            return UP
    elif (blanky == topRow and blankx == 1 and highTx == blankx - 1 and
          lowTx == blankx + 2 and highTy == topRow and lowTy == bottomRow):
        if Qy == bottomRow and Qx == blankx:
            return DOWN
        elif Ry == bottomRow and Rx == blankx:
            return DOWN
        elif Sy == bottomRow and Sx == blankx:
            return DOWN
    elif (blanky == bottomRow and blankx == 2 and highTx == blankx + 1 and
          lowTx == blankx - 2 and highTy == bottomRow and lowTy == topRow):
        if Qy == topRow and Qx == blankx:
            return UP
        elif Ry == topRow and Rx == blankx:
            return UP
        elif Sy == topRow and Sx == blankx:
            return UP

    # 2 of Q,R,S are betw highT and lowT.
    # Want to pull the Q,R,S tile that is betw n1 and n2 into a swap column as
    # quickly as possible; it needs to go betw lowT and highT
    if lowTy == topRow:
        if lowTx == 0:
            if blanky == topRow:
                if blankx in (1, 2):
                    return RIGHT
                elif blankx == 3:
                    return DOWN
            elif blanky == bottomRow:
                if blankx == 3:
                    return LEFT
                elif blankx ==2:
                    pass  # above cross-swap logic applies
                elif blankx in (0, 1):
                    return RIGHT
        elif lowTx == 1:
            if blanky == topRow:
                if blankx in (0, 2):
                    return RIGHT
                elif blankx == 3:
                    return DOWN
            elif blanky == bottomRow:
                if blankx == 0:
                    return UP
                elif blankx in (1, 2, 3):
                    return LEFT
        elif lowTx == 2:
            if blanky == topRow:
                if blankx == 0:
                    return DOWN
                elif blankx in (1, 3):
                    return LEFT
            elif blanky == bottomRow:
                # the tile we want to cross-swap with is in (3, bottomRow)
                if blankx in (0, 1, 2):
                    return RIGHT
                elif blankx == 3:
                    return UP
        elif lowTx == 3:
            if blanky == topRow:
                if blankx in (0, 1):
                    return RIGHT
                elif blankx == 2:
                    pass  # cross-swap logic applies
            elif blanky == bottomRow:
                if blankx in (0, 3):
                    return UP
                elif blankx == 1:
                    return LEFT
                elif blankx == 2:
                    return RIGHT
    elif lowTy == bottomRow:
        if lowTx == 0:
            if blanky == topRow:
                if blankx in (0, 3):
                    return DOWN
                elif blankx == 1:
                    return LEFT
                elif blankx == 2:
                    return RIGHT
            elif blanky == bottomRow:
                if blankx == 1:
                    pass  # cross-swap logic applies
                elif blankx in (2, 3):
                    return LEFT
        elif lowTx == 1:
            if blanky == topRow:
                if blankx == 0:
                    return DOWN
                elif blankx in (1, 2, 3):
                    return LEFT
            elif blanky == bottomRow:
                if blankx in (0, 2):
                    return RIGHT
                elif blankx == 3:
                    return UP
        elif lowTx == 2:
            if blanky == topRow:
                if blankx in (0, 3):
                    return DOWN
                elif blankx in (1, 2):
                    return RIGHT
            elif blanky == bottomRow:
                if blankx in (0, 1):
                    return RIGHT
                elif blankx == 3:
                    return LEFT
        elif lowTx == 3:
            if blanky == topRow:
                if blankx == 0:
                    return RIGHT
                elif blankx == 1:
                    pass  # cross-swap logic applies
                elif blankx in (2, 3):
                    return LEFT
            elif blanky == bottomRow:
                if blankx == 0:
                    return UP
                elif blankx in (1, 2):
                    return LEFT


def fixReversal(lowTx, lowTy, highTx, highTy, n1Tx, n1Ty, n2Tx, n2Ty, Qx, Qy,
                Rx, Ry, Sx, Sy, blankx, blanky, topRow, bottomRow,
                Tax, Tay, Tdx, Tdy, doubleReversal=False):
    """Returns nextMove (one of UP, DOWN, LEFT, RIGHT).  lowT and highT are
    reversed.  n1 and n2 might be reversed.  val(n2T) > val(n1T).  This ftn is
    called from order4 when n1T and n2T can be pushed over to one side enough
    that a cross-swap can be done.  This ftn works if one of Q,R,S or two of
    Q,R,S or three of Q,R,S are betw lowT and highT."""

    # possible cases: TbTa_reversed, TcTb_reversed, TdTc_reversed,
    # TdTa_reversed.

    # This ftn can handle cases where 2 of Q,R,S are betw n1 and n2 if we have
    # one of Q,R,S betw highT and lowT OR if highT and lowT are adjacent and
    # certain further conditions hold.

    # Note: since n1 and n2 get treated exactly the same in the following logic,
    # it does not matter that order4 reverses n1,n2 when they refer to Ta and
    # Td.
    # First see if we can cross-swap with one of Ta,Tb,Tc,Td.
    if blanky == bottomRow:
        if blankx == 1:
            if lowTy == topRow and lowTx == blankx and highTx < lowTx:
                if n1Tx > lowTx and n2Tx > lowTx:
                    return UP
            elif highTy == topRow and highTx == blankx and highTx < lowTx:
                if n1Tx == 0 and n2Tx == 0:
                    return UP
        elif blankx == 2:
            if lowTy == topRow and lowTx == blankx and highTx < lowTx:
                if n1Tx == 3 and n2Tx == 3:
                    return UP
            elif highTy == topRow and highTx == blankx and highTx < lowTx:
                if n1Tx < highTx and n2Tx < highTx:
                    return UP
    elif blanky == topRow:
        if blankx == 1:
            if lowTy == bottomRow and lowTx == blankx and lowTx < highTx:
                if n2Tx == 0 and n1Tx == 0:
                    return DOWN
            elif highTy == bottomRow and highTx == blankx and lowTx < highTx:
                if n1Tx > highTx and n2Tx > highTx:
                    return DOWN
        elif blankx == 2:
            if lowTy == bottomRow and lowTx == blankx and lowTx < highTx:
                if n2Tx < lowTx and n1Tx < lowTx:
                    return DOWN
            elif highTy == bottomRow and highTx == blankx and lowTx < highTx:
                if n1Tx == 3 and n2Tx == 3:
                    return DOWN

    # If fixReversal is called when there is a double reversal, it always works
    # on the TbTa reversal first, not the TdTc reversal.  But oftentimes the
    # swap conditions for the TdTc reversal will be met first as blank moves in
    # the counter-clockwise direction.  The following code permits the cross-
    # swap that fixes the TdTc reversal.
    if doubleReversal:
        lowTx_tmp, lowTy_tmp = lowTx, lowTy
        highTx_tmp, highTy_tmp = highTx, highTy
        highTx, highTy = n2Tx, n2Ty
        lowTx, lowTy = n1Tx, n1Ty
        n2Tx, n2Ty = highTx_tmp, highTy_tmp
        n1Tx, n1Ty = lowTx_tmp, lowTy_tmp
        
        if blanky == bottomRow:
            if blankx == 1:
                if lowTy == topRow and lowTx == blankx and highTx < lowTx:
                    if n1Tx > lowTx and n2Tx > lowTx:
                        return UP
                elif highTy == topRow and highTx == blankx and highTx < lowTx:
                    if n1Tx == 0 and n2Tx == 0:
                        return UP
            elif blankx == 2:
                if lowTy == topRow and lowTx == blankx and highTx < lowTx:
                    if n1Tx == 3 and n2Tx == 3:
                        return UP
                elif highTy == topRow and highTx == blankx and highTx < lowTx:
                    if n1Tx < highTx and n2Tx < highTx:
                        return UP
        elif blanky == topRow:
            if blankx == 1:
                if lowTy == bottomRow and lowTx == blankx and lowTx < highTx:
                    if n2Tx == 0 and n1Tx == 0:
                        return DOWN
                elif highTy == bottomRow and highTx == blankx and lowTx < highTx:
                    if n1Tx > highTx and n2Tx > highTx:
                        return DOWN
            elif blankx == 2:
                if lowTy == bottomRow and lowTx == blankx and lowTx < highTx:
                    if n2Tx < lowTx and n1Tx < lowTx:
                        return DOWN
                elif highTy == bottomRow and highTx == blankx and lowTx < highTx:
                    if n1Tx == 3 and n2Tx == 3:
                        return DOWN

    # Rotate blank until conditions for a cross-swap hold.  Otherwise we likely
    # need completely separate logic based on the number of Q,R,S betw highT
    # and lowT.
    return continueDirCCW(blankx, blanky, topRow, bottomRow)

#############################################################################
### Main function for order4.py:
#############################################################################

def order4(row, board):
    """Returns nextMove (one of UP, DOWN, LEFT, RIGHT).  When this ftn is
    called, Ta-Td are in the same or adjacent rows.  Final positions are in
    the topRow in the following order from left to right: Ta, Tb, Tc, Td.  When
    this ftn is called, these four tiles are NOT in the correct order such that
    they can be "rotated" into their final positions.  This ftn orders these
    four tiles so that readyToRotate returns True.  This ftn is called from 
    getNextMove in slidePuzzle_algorithm_ver01.py.  Ta-Td have yet to be
    "made adjacent".  Blank will be in either the topRow or the bottomRow."""

    blankx, blanky = getPosition(board, BLANK)
    if row == 'first':
        topRow, bottomRow = 0, 1
        Tax, Tay = getPosition(board, 1)
        Tbx, Tby = getPosition(board, 2)
        Tcx, Tcy = getPosition(board, 3)
        Tdx, Tdy = getPosition(board, 4)
    elif row == 'second':
        topRow, bottomRow = 1, 2
        Tax, Tay = getPosition(board, 5)
        Tbx, Tby = getPosition(board, 6)
        Tcx, Tcy = getPosition(board, 7)
        Tdx, Tdy = getPosition(board, 8)
    elif row == 'third':
        topRow, bottomRow = 2, 3
        Tax, Tay = getPosition(board, 9)
        Tbx, Tby = getPosition(board, 10)
        Tcx, Tcy = getPosition(board, 11)
        Tdx, Tdy = getPosition(board, 12)

    board_positions = {(0, topRow), (1, topRow), (2, topRow), (3, topRow),
                       (0, bottomRow), (1, bottomRow), (2, bottomRow),
                       (3, bottomRow)}
    remaining_positions = board_positions - {(Tax, Tay), (Tbx, Tby), (Tcx, Tcy),
                                             (Tdx, Tdy), (blankx, blanky)}
    # Get the locations of Q, R, and S.
    remainder = list(remaining_positions)
    Qx, Qy = remainder[0][0], remainder[0][1]
    Rx, Ry = remainder[1][0], remainder[1][1]
    Sx, Sy = remainder[2][0], remainder[2][1]

    tileDict = {'Ta': (Tax, Tay), 'Tb': (Tbx, Tby), 'Tc': (Tcx, Tcy),
                'Td': (Tdx, Tdy), 'blank': (blankx, blanky), 'Q': (Qx, Qy),
                'R': (Rx, Ry), 'S': (Sx, Sy), (Tax, Tay): 'Ta', (Tbx, Tby): 'Tb',
                (Tcx, Tcy): 'Tc', (Tdx, Tdy): 'Td', (blankx, blanky): 'blank',
                (Qx, Qy): 'Q', (Rx, Ry): 'R', (Sx, Sy): 'S'}

    # generate list of reversed tiles:
    reversedTs = getTrueReversedTs(Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx, Tdy,
                                   blankx, blanky, Qx, Qy, Rx, Ry, Sx, Sy,
                                   topRow, bottomRow)
    try:
        if len(reversedTs) > 2:
            raise ValueError
    except ValueError:
        print("ERROR: (ftn= order4) Should not have more than 2 reversed tuples.")

    # len(reversedTs) == 1 or len(reversedTs) == 2.  The length won't ever
    # be 0 when this ftn is called.
    if len(reversedTs) == 1:
        # tile with smaller value comes first in the tuple; the tuple has the
        # form of ('Tb','Tc'); however, when we have a TdTa reversal,
        # highT = Ta and lowT = Td (the  tuple is returned as ('Td', 'Ta')).
        # The latter is done in order to handle the logic around putTbetwSpec.
        # See unit tests 23-26.
        lowT, highT = reversedTs[0][0], reversedTs[0][1]
        lowTx, lowTy = tileDict[lowT]
        highTx, highTy = tileDict[highT]
        highIsTa = (highTx, highTy) == (Tax, Tay)
        lowIsTd = (lowTx, lowTy) == (Tdx, Tdy)
        TdTa_reversed = highIsTa and lowIsTd

        # possible cases: TbTa_reversed, TcTb_reversed, TdTc_reversed,
        # TdTa_reversed.

        # Identify the non-reversed tiles:
        non_reversed = {(Tax, Tay), (Tbx, Tby), (Tcx, Tcy),
                        (Tdx, Tdy)} - {(lowTx, lowTy), (highTx, highTy)}
        non_rev = list(non_reversed)
        n1Tx, n1Ty = non_rev[0][0], non_rev[0][1]
        n2Tx, n2Ty = non_rev[1][0], non_rev[1][1]
        n1IsTa = (n1Tx, n1Ty) == (Tax, Tay)
        n2IsTd = (n2Tx, n2Ty) == (Tdx, Tdy)
        # For debugging purposes it is helpful if n2 refers to the non-reversed
        # tile with the larger value.
        n2_val, n1_val = board[n2Tx][n2Ty], board[n1Tx][n1Ty]
        if n1_val > n2_val:
            Tx, Ty = n1Tx, n1Ty
            n1Tx, n1Ty = n2Tx, n2Ty
            n2Tx, n2Ty = Tx, Ty
        # Conditions for calling putTbetwSpec require that we have n2 = Ta and
        # n1 = Td.
        if n1IsTa and n2IsTd:
            Tx, Ty = n1Tx, n1Ty
            n1Tx, n1Ty = n2Tx, n2Ty
            n2Tx, n2Ty = Tx, Ty

        # Generally, when the non-reversed tiles are close together, we can
        # move them over to one side and call fixReversal.  ("Close together"
        # means satisfying either n1n2_adj or test2 below.  A direct
        # cross-swap can also be done if 2 of Q,R,S are betw n1 and n2, but
        # certain other conditions have to hold.)  The cross-swap fixes the
        # reversal.
        
        # If highT and lowT are adjacent AND there are 2 of Q,R,S betw n1 and
        # n2, we might need to put one of Q,R,S betw highT and lowT before we
        # call fixReversal.  If all of Q,R,S are betw n1 and n2, a call to
        # putTileBetw is required.  If all of Q,R,S are betw highT and lowT, a
        # call to putTileBetw is NOT required.
        
        # When both n1n2_adj and test2 are false, there are at least 2 of
        # Q,R,S betw n1 and n2.
        n1n2_adj = adjacent2(n1Tx, n1Ty, n2Tx, n2Ty, blankx, blanky)
        test2 = QRSbetw(n1Tx, n1Ty, n2Tx, n2Ty, Qx, Qy, Rx, Ry, Sx, Sy, blankx,
                        blanky, topRow, bottomRow)

        highLow_adj = adjacent2(highTx, highTy, lowTx, lowTy, blankx, blanky)
        
        n1High_adj = adjacent2(highTx, highTy, n1Tx, n1Ty, blankx, blanky)
        n2Low_adj = adjacent2(lowTx, lowTy, n2Tx, n2Ty, blankx, blanky)
        
        # See unit tests 23 - 26 for why we need the following.  A call to
        # putTbetwSpec is required when both n2High_adj and
        # n1Low_adj are true AND when there are 2 of Q,R,S betw highT and
        # lowT.
        n2High_adj = adjacent2(highTx, highTy, n2Tx, n2Ty, blankx, blanky)
        n1Low_adj = adjacent2(lowTx, lowTy, n1Tx, n1Ty, blankx, blanky)
        
        # When Td,Ta are reversed, highT and lowT are reversed.  So we need to
        # account for this in n1High_adj and n2Low_adj.
        if TdTa_reversed:
            n1High_adj = n1Low_adj
            n2Low_adj = n2High_adj
        # When Tc,Tb are reversed, we also need to "correct" n1High_adj
        # and n2Low_adj because n1 now refers to Td and n2 refers to Ta.
        if highT == 'Tc' and lowT == 'Tb':
            n1High_adj = adjacent2(highTx, highTy, n2Tx, n2Ty, blankx, blanky)
            n2Low_adj = adjacent2(lowTx, lowTy, n1Tx, n1Ty, blankx, blanky)

        QRS_cont = adjacent3(Qx, Qy, Rx, Ry, Sx, Sy, blankx, blanky)
        RSQ_cont = adjacent3(Rx, Ry, Sx, Sy, Qx, Qy, blankx, blanky)
        SQR_cont = adjacent3(Sx, Sy, Qx, Qy, Rx, Ry, blankx, blanky)
        QRS_adj = QRS_cont or RSQ_cont or SQR_cont
        allQRSbetw_n1n2 = QRS_adj and not n1n2_adj
        # allQRSbetw_highLow = QRS_adj and not highLow_adj

        if QRS_adj:
            if allQRSbetw_n1n2:
                # insert tile betw highT and lowT
                nextMove = putTileBetw(highTx, highTy, lowTx, lowTy, blankx,
                                       blanky, Qx, Qy, Rx, Ry, Sx, Sy, topRow,
                                       bottomRow)
                return nextMove
            else:
                nextMove = fixReversal(lowTx, lowTy, highTx, highTy, n1Tx,
                                       n1Ty, n2Tx, n2Ty, Qx, Qy, Rx, Ry, Sx,
                                       Sy, blankx, blanky, topRow, bottomRow,
                                       Tax, Tay, Tdx, Tdy)
                return nextMove
        elif not QRS_adj:
            if not highLow_adj:
                # See unit tests 23-26.  In unit test 23 we have a TbTa reversal
                # with 2 of Q,R,S betw Ta,Tb but, because Ta,Tc are adjacent
                # and Tb,Td are adjacent, we are not able to do a cross-swap.
                if not (n2High_adj and n1Low_adj and test2):
                    nextMove = fixReversal(lowTx, lowTy, highTx, highTy, n1Tx,
                                           n1Ty, n2Tx, n2Ty, Qx, Qy, Rx, Ry,
                                           Sx, Sy, blankx, blanky, topRow,
                                           bottomRow, Tax, Tay, Tdx, Tdy)
                    return nextMove
                else:
                    # We want all of Q,R,S betw highT and lowT; at present,
                    # 2 of Q,R,S are betw highT and lowT
                    nextMove = putTbetwSpec(highTx, highTy, lowTx, lowTy,
                                            blankx, blanky, topRow, bottomRow,
                                            Qx, Qy, Rx, Ry, Sx, Sy)
                    return nextMove
            elif highLow_adj:
                if not n1n2_adj and not test2:
                    # exactly 2 of Q,R,S are betw n1 and n2
                    if n2Low_adj or n1High_adj:
                        nextMove = fixReversal(lowTx, lowTy, highTx, highTy,
                                               n1Tx, n1Ty, n2Tx, n2Ty, Qx, Qy,
                                               Rx, Ry, Sx, Sy, blankx, blanky,
                                               topRow, bottomRow, Tax, Tay, Tdx, Tdy)
                        return nextMove
                    else:
                        nextMove = putTileBetw(highTx, highTy, lowTx, lowTy,
                                               blankx, blanky, Qx, Qy, Rx, Ry,
                                               Sx, Sy, topRow, bottomRow)
                        return nextMove
                else:
                    # n1 and n2 are adjacent, or exactly one of Q,R,S is betw
                    # them; this is when it is easiest to push n1, n2 over to
                    # one side in order to execute the necessary cross-swap
                    nextMove = fixReversal(lowTx, lowTy, highTx, highTy, n1Tx,
                                           n1Ty, n2Tx, n2Ty, Qx, Qy, Rx, Ry, Sx,
                                           Sy, blankx, blanky, topRow, bottomRow,
                                           Tax, Tay, Tdx, Tdy)
                    return nextMove
    elif len(reversedTs) == 2:
        # possible cases: (i) TbTa_reversed; (ii) TdTc_reversed
        doubleReversal = True

        # if Q,R,S are contiguous, a call to putTileBetw is required
        QRS_cont = adjacent3(Qx, Qy, Rx, Ry, Sx, Sy, blankx, blanky)
        RSQ_cont = adjacent3(Rx, Ry, Sx, Sy, Qx, Qy, blankx, blanky)
        SQR_cont = adjacent3(Sx, Sy, Qx, Qy, Rx, Ry, blankx, blanky)
        QRS_adj = QRS_cont or RSQ_cont or SQR_cont
        
        TbTa_adj = adjacent2(Tbx, Tby, Tax, Tay, blankx, blanky)
        TdTc_adj = adjacent2(Tdx, Tdy, Tcx, Tcy, blankx, blanky)
        # following is equal to n2High_adj:
        TdTb_adj = adjacent2(Tdx, Tdy, Tbx, Tby, blankx, blanky)
        # following is equal to n1Low_adj:
        TcTa_adj = adjacent2(Tcx, Tcy, Tax, Tay, blankx, blanky)
        # the following is equal to n1High_adj:
        TcTb_adj = adjacent2(Tbx, Tby, Tcx, Tcy, blankx, blanky)
        # the following is equal to n2Low_adj:
        TdTa_adj = adjacent2(Tax, Tay, Tdx, Tdy, blankx, blanky)
        
        allQRSbetw_TdTc = QRS_adj and not TdTc_adj

        # if both TdTc_adj and test2 are false, we have at least 2 of
        # Q,R,S betw Td, Tc.
        test2 = QRSbetw(Tcx, Tcy, Tdx, Tdy, Qx, Qy, Rx, Ry, Sx, Sy, blankx,
                        blanky, topRow, bottomRow)
        
        # focus on the TbTa reversal; the following code mimicks the code in
        # the above section (len(reversedTs) == 1).
        if QRS_adj:
            if allQRSbetw_TdTc:  # equivalent to allQRSbetw_n1n2
                # insert tile betw Tb and Ta
                nextMove = putTileBetw(Tbx, Tby, Tax, Tay, blankx, blanky, Qx,
                                       Qy, Rx, Ry, Sx, Sy, topRow, bottomRow)
                return nextMove
            else:
                nextMove = fixReversal(Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx, Tdy,
                                       Qx, Qy, Rx, Ry, Sx, Sy, blankx, blanky,
                                       topRow, bottomRow, Tax, Tay, Tdx, Tdy,
                                       doubleReversal)
                return nextMove
        elif not QRS_adj:
            if not TbTa_adj:
                # If we have a TbTa and a TcTd reversal, with 2 of Q,R,S betw
                # Ta,Tb, and we have TdTa_adj, TcTb_adj, and test2 == True, we
                # are not able to do a cross-swap.
                if not(TdTa_adj and TcTb_adj and test2):
                    nextMove = fixReversal(Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx, Tdy,
                                           Qx, Qy, Rx, Ry, Sx, Sy, blankx, blanky,
                                           topRow, bottomRow, Tax, Tay, Tdx,
                                           Tdy, doubleReversal)
                    return nextMove
                else:
                    # We want all of Q,R,S betw Tb and Ta; at present, 2 of
                    # Q,R,S are betw Tb and Ta
                    nextMove = putTbetwSpec(Tbx, Tby, Tax, Tay, blankx, blanky,
                                            topRow, bottomRow, Qx, Qy, Rx, Ry,
                                            Sx, Sy)
                    return nextMove
            elif TbTa_adj:
                if not TdTc_adj and not test2:
                    # exactly 2 of Q,R,S are betw Tc and Td
                    if TdTa_adj or TcTb_adj:
                        nextMove = fixReversal(Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx, Tdy,
                                               Qx, Qy, Rx, Ry, Sx, Sy, blankx, blanky,
                                               topRow, bottomRow, Tax, Tay, Tdx,
                                               Tdy, doubleReversal)
                        return nextMove
                    else:
                        nextMove = putTileBetw(Tbx, Tby, Tax, Tay,
                                               blankx, blanky, Qx, Qy, Rx, Ry,
                                               Sx, Sy, topRow, bottomRow)
                        return nextMove
                else:
                    # n1 (Tc) and n2 (Td) are adjacent, or exactly one of Q,R,S
                    # is betw them; this is when it is easiest to push n1, n2
                    # over to one side in order to execute the necessary cross-swap
                    nextMove = fixReversal(Tax, Tay, Tbx, Tby, Tcx, Tcy, Tdx,
                                           Tdy, Qx, Qy, Rx, Ry, Sx, Sy,
                                           blankx, blanky, topRow, bottomRow,
                                           Tax, Tay, Tdx, Tdy, doubleReversal)
                    return nextMove


#############################################################################
###
#############################################################################
