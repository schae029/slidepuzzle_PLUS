# -*- coding: utf-8 -*-
"""
@author: Greg Schaefer

module name: getTiles.py

module contents (9 ftns):

    - getDisplaced
    - moveRLDefault
    - getRLTiles
    - moveRLDbotRow
    - getLargestValCol
    - moveRLDbotRowAdj
    - moveRLDtopRow
    - getTiles
    - bubbleUp
    
Released under a GNU GPLv3 license. 

"""

#############################################################################
### getTiles.py COPYRIGHT:
#############################################################################

# SlidePuzzlePlus, getTiles.py
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
### getTiles.py
#############################################################################

from constants_and_genFtns import *

#############################################################################
### Helper ftns
#############################################################################

def getDisplaced(Tay, Tby, Tcy, Tdy, blanky, topRow, bottomRow):
    """Returns list of up to 5 tiles not in topRow or bottomRow.  Tiles in list
    will be any of Ta-Td and blank."""
    returnedList = []
    if Tay not in (topRow, bottomRow):
        returnedList.append('Ta')
    if Tby not in (topRow, bottomRow):
        returnedList.append('Tb')
    if Tcy not in (topRow, bottomRow):
        returnedList.append('Tc')
    if Tdy not in (topRow, bottomRow):
        returnedList.append('Td')
    if blanky not in (topRow, bottomRow):
        returnedList.append('blank')

    return returnedList


def moveRLDefault(blankx, Tx, default_dir):
    """Returns nextMove (one of RIGHT, LEFT, default_dir).  If blanky = Ty - 1,
    would like to move blank above T (i.e., have blankx = Tx)."""

    try:
        if Tx is None:
            raise ValueError
    except ValueError:
        print("ERROR: (ftn= moveRLDefault) Tile column is None.")

    if blankx < Tx:
        if blankx in (0, 1, 2):
            return RIGHT
        else:
            return default_dir
    elif blankx > Tx:
        if blankx in (1, 2, 3):
            return LEFT
        else:
            return default_dir
    elif blankx == Tx:
        return default_dir


def getRLTiles(blankx, tilesInPlace, tileRow):
    """Returns 2 lists: first is tilesInPlace in tileRow to the left of blankx;
    second is tilesInPlace in tileRow to the right of blankx."""
    if blankx == 0:
        tilesToLeft = {}
        tilesToRight = tilesInPlace & {(1, tileRow), (2, tileRow), (3, tileRow)}
    elif blankx == 1:
        tilesToLeft = tilesInPlace & {(0, tileRow)}
        tilesToRight = tilesInPlace & {(2, tileRow), (3, tileRow)}
    elif blankx == 2:
        tilesToLeft = tilesInPlace & {(0, tileRow), (1, tileRow)}
        tilesToRight = tilesInPlace & {(3, tileRow)}
    elif blankx == 3:
        tilesToLeft = tilesInPlace & {(0, tileRow), (1, tileRow), (2, tileRow)}
        tilesToRight = {}
        
    return list(tilesToLeft), list(tilesToRight)


def moveRLDbotRow(blankx, blanky, highTx, endTiles, tsInNextRow, tsInBotRow,
                  board, lastMove):
    """Returns nextMove (one of RIGHT, LEFT, DOWN) when one or more tiles are
    in place in the bottomRow, blanky = bottomRow, and we have one or more
    target tiles in the nextRow which we want to move into the bottomRow without
    creating a reversal.  This means we may want to shift the tsInBotRow to
    right or left.  When this ftn is called, blanky is in (1, 2).  If
    blanky = 1, we are working on the first row; if blanky = 2, we are working
    on the second row.  By default, this ftn pulls highT into bottomRow.
    blank moves into nextRow only if it brings a rowTile into bottomRow."""

    nextMove = None
    Tax, Tay = endTiles[0][0], endTiles[0][1]
    Tdx, Tdy = endTiles[1][0], endTiles[1][1]
    tsToLeft, tsToRight = getRLTiles(blankx, tsInBotRow, blanky)
    Ta_val, Td_val = board[Tax][Tay], board[Tdx][Tdy]

    if blankx == 0:
        # We have to move down or to the right.  If we move to the right,
        # next decision is made under the blankx == 1 section below.
        topC1 = (1, blanky) in tsToRight
        topC2 = (2, blanky) in tsToRight
        topC3 = (3, blanky) in tsToRight
        botC0 = (0, blanky + 1) in tsInNextRow
        botC1 = (1, blanky + 1) in tsInNextRow
        botC2 = (2, blanky + 1) in tsInNextRow
        # don't bother with tile to far right
#        botC3 = (3, blanky + 1) in tsInNextRow

        if topC1 or topC2 or topC3:
            if topC1:
                tcol = 1
            elif topC2:
                tcol = 2
            elif topC3:
                tcol = 3
            inPlace_val = board[tcol][blanky]
            inPlaceIsTa = inPlace_val == Ta_val
            inPlaceIsTd = inPlace_val == Td_val
            if botC0:
                elem_val = board[0][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if (inPlaceIsTd and elemIsTa) or lastMove == LEFT:
                    nextMove = DOWN
                    return DOWN  # Ta now to left of Td in bottomRow
                elif not(inPlaceIsTa and elemIsTd):
                    if elem_val > inPlace_val or lastMove == LEFT:
                        nextMove = DOWN
                        return DOWN
                    elif lastMove != LEFT:
                        nextMove = RIGHT
                        return RIGHT
                elif lastMove != LEFT:
                    nextMove = RIGHT
                    return RIGHT
            if botC1 or botC2:  # use 'if' here, not elif
                if botC1:
                    column = 1
                elif botC2:
                    column = 2
                elem_val = board[column][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if inPlaceIsTa and elemIsTd:
                    nextMove = RIGHT
                    return RIGHT
                elif not(inPlaceIsTd and elemIsTa):
                    if elem_val < inPlace_val:
                        nextMove = RIGHT
                        return RIGHT  # moves lower-val tile over to left
        if nextMove is None or nextMove == oppDirection(lastMove):
            if blankx == highTx:
                return DOWN
            else:
                return RIGHT  # we want to pull in a tile from nextRow
    elif blankx == 1:
        topC0 = (0, blanky) in tsToLeft
        topC2 = (2, blanky) in tsToRight
        topC3 = (3, blanky) in tsToRight
        botC0 = (0, blanky + 1) in tsInNextRow
        botC1 = (1, blanky + 1) in tsInNextRow
        botC2 = (2, blanky + 1) in tsInNextRow
        botC3 = (3, blanky + 1) in tsInNextRow

        if topC0:
            inPlace_val = board[0][blanky]
            inPlaceIsTa = inPlace_val == Ta_val
            inPlaceIsTd = inPlace_val == Td_val
            if botC0:
                elem_val = board[0][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if inPlaceIsTd and elemIsTa:
                    nextMove = LEFT
                    return LEFT
                elif not(inPlaceIsTa and elemIsTd):
                    if elem_val > inPlace_val:
                        nextMove = LEFT
                        return LEFT
            if botC1:  # again, use 'if' and not elif
                elem_val = board[1][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if inPlaceIsTa and elemIsTd:
                    nextMove = DOWN
                    return DOWN
                elif not(inPlaceIsTd and elemIsTa):
                    if elem_val < inPlace_val:
                        nextMove = DOWN
                        return DOWN  # don't worry about rowTs to right in bottomRow
            if botC2:
                elem_val = board[2][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if not topC2:
                    if inPlaceIsTa and elemIsTd:
                        nextMove = RIGHT
                        return RIGHT
                    elif not(inPlaceIsTd and elemIsTa):
                        if elem_val < inPlace_val:
                            nextMove = RIGHT
                            return RIGHT
                elif topC2:  # rowTs in topC0 and topC2
                    topC2_val = board[2][blanky]
                    topC2IsTa = topC2_val == Ta_val
                    topC2IsTd = topC2_val == Td_val
                    if topC2IsTa and elemIsTd:
                        nextMove = RIGHT
                        return RIGHT
                    elif not(topC2IsTd and elemIsTa):
                        if elem_val < topC2_val:
                            nextMove = RIGHT
                            return RIGHT
        if topC2 or topC3:
            if topC2:
                tcol = 2
            elif topC3:
                tcol = 3
            inPlace_val = board[tcol][blanky]
            inPlaceIsTa = inPlace_val == Ta_val
            inPlaceIsTd = inPlace_val == Td_val
            if botC1:
                elem_val = board[1][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if inPlaceIsTd and elemIsTa:
                    nextMove = DOWN
                    return DOWN
                elif not(inPlaceIsTa and elemIsTd):
                    if elem_val > inPlace_val:
                        nextMove = DOWN
                        return DOWN
            if botC2:
                elem_val = board[2][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if inPlaceIsTa and elemIsTd:
                    nextMove = RIGHT
                    return RIGHT
                elif not(inPlaceIsTd and elemIsTa):
                    if elem_val < inPlace_val:
                        nextMove = RIGHT
                        return RIGHT
            if botC3:
                elem_val = board[3][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if not topC3:
                    if inPlaceIsTa and elemIsTd:
                        nextMove = RIGHT
                        return RIGHT
                    elif not(inPlaceIsTd and elemIsTa):
                        if elem_val < inPlace_val:
                            nextMove = RIGHT
                            return RIGHT
                elif topC3:
                    topC3_val = board[3][blanky]
                    topC3IsTa = topC3_val == Ta_val
                    topC3IsTd = topC3_val == Td_val
                    if topC3IsTa and elemIsTd:
                        nextMove = RIGHT
                        return RIGHT
                    elif not(topC3IsTd and elemIsTa):
                        if elem_val < topC3_val:
                            nextMove = RIGHT
                            return RIGHT
        if nextMove is None or nextMove == oppDirection(lastMove):
            if blankx == highTx:
                return DOWN
            elif blankx < highTx:
                return RIGHT
            elif blankx > highTx:
                return LEFT
    elif blankx == 2:
        topC0 = (0, blanky) in tsToLeft
        topC1 = (1, blanky) in tsToLeft
        topC3 = (3, blanky) in tsToRight
        botC0 = (0, blanky + 1) in tsInNextRow
        botC1 = (1, blanky + 1) in tsInNextRow
        botC2 = (2, blanky + 1) in tsInNextRow
        botC3 = (3, blanky + 1) in tsInNextRow
        # focus on closest tiles first
        if topC1:
            inPlace_val = board[1][blanky]
            inPlaceIsTa = inPlace_val == Ta_val
            inPlaceIsTd = inPlace_val == Td_val
            if botC2:
                elem_val = board[2][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if inPlaceIsTa and elemIsTd:
                    nextMove = DOWN
                    return DOWN
                elif not(inPlaceIsTd and elemIsTa):
                    if elem_val < inPlace_val:
                        nextMove = DOWN
                        return DOWN
            if botC1:
                elem_val = board[1][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if inPlaceIsTd and elemIsTa:
                    nextMove = LEFT
                    return LEFT
                elif not(inPlaceIsTa and elemIsTd):
                    if elem_val > inPlace_val:
                        nextMove = LEFT
                        return LEFT
            if botC3:
                elem_val = board[3][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if not topC3:
                    if inPlaceIsTa and elemIsTd:
                        nextMove = RIGHT
                        return RIGHT
                    elif not(inPlaceIsTd and elemIsTa):
                        if elem_val < inPlace_val:
                            nextMove = RIGHT
                            return RIGHT
                elif topC3:  # rowTs in topC1 and topC3
                    topC3_val = board[3][blanky]
                    topC3IsTa = topC3_val == Ta_val
                    topC3IsTd = topC3_val == Td_val
                    if topC3IsTa and elemIsTd:
                        nextMove = RIGHT
                        return RIGHT
                    elif not(topC3IsTd and elemIsTa):
                        if elem_val < topC3_val:
                            nextMove = RIGHT
                            return RIGHT
        if topC3:
            inPlace_val = board[3][blanky]
            inPlaceIsTa = inPlace_val == Ta_val
            inPlaceIsTd = inPlace_val == Td_val
            if botC2:
                elem_val = board[2][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if inPlaceIsTd and elemIsTa:
                    nextMove = DOWN
                    return DOWN
                elif not(inPlaceIsTa and elemIsTd):
                    if elem_val > inPlace_val:
                        nextMove = DOWN
                        return DOWN
            if botC3:
                elem_val = board[3][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if inPlaceIsTa and elemIsTd:
                    nextMove = RIGHT
                    return RIGHT
                elif not(inPlaceIsTd and elemIsTa):
                    if elem_val < inPlace_val:
                        nextMove = RIGHT
                        return RIGHT
            if botC1:
                elem_val = board[1][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if not topC1:
                    if inPlaceIsTd and elemIsTa:
                        nextMove = LEFT
                        return LEFT
                    elif not(inPlaceIsTa and elemIsTd):
                        if elem_val > inPlace_val:
                            nextMove = LEFT
                            return LEFT
                elif topC1:  # rowTs in topC1 and topC3
                    topC1_val = board[1][blanky]
                    topC1IsTa = topC1_val == Ta_val
                    topC1IsTd = topC1_val == Td_val
                    if topC1IsTd and elemIsTa:
                        nextMove = LEFT
                        return LEFT
                    elif not(topC1IsTa and elemIsTd):
                        if elem_val > topC1_val:
                            nextMove = LEFT
                            return LEFT
        if topC0:
            inPlace_val = board[0][blanky]
            inPlaceIsTa = inPlace_val == Ta_val
            inPlaceIsTd = inPlace_val == Td_val
            if botC2:
                elem_val = board[2][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if inPlaceIsTa and elemIsTd:
                    nextMove = DOWN
                    return DOWN
                elif not(inPlaceIsTd and elemIsTa):
                    if elem_val < inPlace_val:
                        nextMove = DOWN
                        return DOWN
            if botC3:
                elem_val = board[3][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if not topC3:
                    if inPlaceIsTa and elemIsTd:
                        nextMove = RIGHT
                        return RIGHT
                    elif not(inPlaceIsTd and elemIsTa):
                        if elem_val < inPlace_val:
                            nextMove = RIGHT
                            return RIGHT
                elif topC3:  # rowTs in topC0 and topC3
                    topC3_val = board[3][blanky]
                    topC3IsTa = topC3_val == Ta_val
                    topC3IsTd = topC3_val == Td_val
                    if topC3IsTa and elemIsTd:
                        nextMove = RIGHT
                        return RIGHT
                    elif not(topC3IsTd and elemIsTa):
                        if elem_val < topC3_val:
                            nextMove = RIGHT
                            return RIGHT
            if botC1:
                elem_val = board[1][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if not topC1:
                    if inPlaceIsTa and elemIsTd:
                        nextMove = LEFT
                        return LEFT
                    elif not(inPlaceIsTd and elemIsTa):
                        if elem_val < inPlace_val:
                            nextMove = LEFT
                            return LEFT
                elif topC1:  # rowTs in topC0 and topC1
                    topC1_val = board[1][blanky]
                    topC1IsTa = topC1_val == Ta_val
                    topC1IsTd = topC1_val == Td_val
                    if topC1IsTd and elemIsTa:
                        nextMove = LEFT
                        return LEFT
                    elif not(topC1IsTa and elemIsTd):
                        if elem_val > topC1_val:
                            nextMove = LEFT
                            return LEFT
            # do not bother with botC0
        if nextMove is None or nextMove == oppDirection(lastMove):
            if blankx == highTx:
                return DOWN
            elif blankx < highTx:
                return RIGHT
            elif blankx > highTx:
                return LEFT
    elif blankx == 3:
        topC0 = (0, blanky) in tsToLeft
        topC1 = (1, blanky) in tsToLeft
        topC2 = (2, blanky) in tsToLeft
        botC1 = (1, blanky + 1) in tsInNextRow
        botC2 = (2, blanky + 1) in tsInNextRow
        botC3 = (3, blanky + 1) in tsInNextRow
        # give priority to tiles nearest blank
        if topC2 or topC1 or topC0:
            if topC2:
                tcol = 2
            elif topC1:
                tcol = 1
            elif topC0:
                tcol = 0
            inPlace_val = board[tcol][blanky]
            inPlaceIsTa = inPlace_val == Ta_val
            inPlaceIsTd = inPlace_val == Td_val
            if botC3:
                elem_val = board[3][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if (inPlaceIsTa and elemIsTd) or lastMove == RIGHT:
                    nextMove = DOWN
                    return DOWN
                elif not(inPlaceIsTd and elemIsTa):
                    if elem_val < inPlace_val or lastMove == RIGHT:
                        nextMove = DOWN
                        return DOWN
                    elif lastMove != RIGHT:
                        nextMove = LEFT
                        return LEFT
                elif lastMove != RIGHT:
                    nextMove = LEFT
                    return LEFT
            if botC1 or botC2:  # use 'if' here, not elif
                if botC2:
                    column = 2
                elif botC1:
                    column = 1
                elem_val = board[column][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if inPlaceIsTd and elemIsTa:
                    nextMove = LEFT
                    return LEFT
                elif not(inPlaceIsTa and elemIsTd):
                    if elem_val > inPlace_val:
                        nextMove = LEFT
                        return LEFT  # moves higher-val tile over to right
        if nextMove is None or nextMove == oppDirection(lastMove):
            if blankx == highTx:
                return DOWN
            else:
                return LEFT  # we are in column 3


def getLargestValCol(tiles, board, endTiles, rowOfBlank):
    """Returns column number for tile in tiles with the largest value.  If the
    tiles set contains both Td and Ta, Ta is selected as the tile with largest
    value if it is in columns 2 or 3 and rowOfBlank = 'top', since in this case
    tiles are being moved from the bottomRow into the topRow and if Ta and Td
    are in the topRow, we want Ta to be to the right of Td.."""
    # tiles is a set with maximum length of 4
    tList = list(tiles)
    Tax, Tay = endTiles[0][0], endTiles[0][1]
    Tdx, Tdy = endTiles[1][0], endTiles[1][1]
    TdTa_present = (Tax, Tay) in tList and (Tdx, Tdy) in tList

    if len(tList) == 1:
        return tList[0][0]
    elif len(tList) == 2:
        t1x, t1y = tList[0][0], tList[0][1]
        t2x, t2y = tList[1][0], tList[1][1]
        t1_val, t2_val = board[t1x][t1y], board[t2x][t2y]
        maxTile_val = max(t1_val, t2_val)
        if maxTile_val == t1_val:
            maxTile_col = t1x
            minTile_col = t2x
        else:
            maxTile_col = t2x
            minTile_col = t1x

        if TdTa_present and Tax in (2, 3) and rowOfBlank == 'top':
            return minTile_col
        else:
            return maxTile_col
    elif len(tList) == 3:
        t1x, t1y = tList[0][0], tList[0][1]
        t2x, t2y = tList[1][0], tList[1][1]
        t3x, t3y = tList[2][0], tList[2][1]
        t1_val, t2_val, t3_val = board[t1x][t1y], board[t2x][t2y], board[t3x][t3y]
        maxTile_val = max(t1_val, t2_val, t3_val)
        minTile_val = min(t1_val, t2_val, t3_val)

        if maxTile_val == t1_val:
            maxTile_col = t1x
        elif maxTile_val == t2_val:
            maxTile_col = t2x
        elif maxTile_val == t3_val:
            maxTile_col = t3x

        if minTile_val == t1_val:
            minTile_col = t1x
        elif minTile_val == t2_val:
            minTile_col = t2x
        elif minTile_val == t3_val:
            minTile_col = t3x

        if TdTa_present and Tax in (2, 3) and rowOfBlank == 'top':
            return minTile_col
        else:
            return maxTile_col
    elif len(tList) == 4:
        t1x, t1y = tList[0][0], tList[0][1]
        t2x, t2y = tList[1][0], tList[1][1]
        t3x, t3y = tList[2][0], tList[2][1]
        t4x, t4y = tList[3][0], tList[3][1]
        t1_val, t2_val, t3_val = board[t1x][t1y], board[t2x][t2y], board[t3x][t3y]
        t4_val = board[t4x][t4y]
        maxTile_val = max(t1_val, t2_val, t3_val, t4_val)
        minTile_val = min(t1_val, t2_val, t3_val, t4_val)

        if maxTile_val == t1_val:
            maxTile_col = t1x
        elif maxTile_val == t2_val:
            maxTile_col = t2x
        elif maxTile_val == t3_val:
            maxTile_col = t3x
        elif maxTile_val == t4_val:
            maxTile_col = t4x

        if minTile_val == t1_val:
            minTile_col = t1x
        elif minTile_val == t2_val:
            minTile_col = t2x
        elif minTile_val == t3_val:
            minTile_col = t3x
        elif minTile_val == t4_val:
            minTile_col = t4x

        if TdTa_present and Tax in (2, 3) and rowOfBlank == 'top':
            return minTile_col
        else:
            return maxTile_col
    else:
        try:
            if len(tList) == 0:
                raise ValueError
        except ValueError:
            print("ERROR: (ftn= getLargestValCol) The length of 'tiles' should be between one and four.")


def moveRLDbotRowAdj(T_val, blankx, blanky, tsInBotRow, board, lastMove):
    """Returns nextMove (one of RIGHT, LEFT, DOWN) when row = 'first', blank
    is in row 1 and the target tile, T, is in row 3.  This ftn aims to arrange
    bottomRow before retrieving T; idea is to increase likelihood that T, when
    inserted into bottomRow, will not create a reversal."""
    # blanky = 1
    C0 = (0, 1) in tsInBotRow
    C1 = (1, 1) in tsInBotRow
    C2 = (2, 1) in tsInBotRow
    C3 = (3, 1) in tsInBotRow
    TisTa = T_val == 1
    TisTd = T_val == 4
    nextMove = None

    if blankx == 0:
        if C1 or C2 or C3:
            if C1:
                C_val = board[1][1]
            elif C2:
                C_val = board[2][1]
            elif C3:
                C_val = board[3][1]
            CisTa = C_val == 1
            CisTd = C_val == 4
            if TisTa and CisTd:
                nextMove = DOWN
                return DOWN
            elif C_val > T_val:
                nextMove = RIGHT
                return RIGHT
        if nextMove is None or nextMove == oppDirection(lastMove):
            return DOWN
    elif blankx == 1:
        if C0:
            C_val = board[0][1]
            CisTa = C_val == 1
            CisTd = C_val == 4
            if TisTa and CisTd:
                nextMove = LEFT
                return LEFT
            elif C_val > T_val:
                nextMove = DOWN
                return DOWN
        if C2 or C3:
            if C2:
                C_val = board[2][1]
            elif C3:
                C_val = board[3][1]
            CisTa = C_val == 1
            CisTd = C_val == 4
            if TisTa and CisTd:
                nextMove = DOWN
                return DOWN
            elif C_val > T_val:
                nextMove = RIGHT
                return RIGHT
        if nextMove is None or nextMove == oppDirection(lastMove):
            return DOWN
    elif blankx == 2:
        if C3:
            C_val = board[3][1]
            CisTa = C_val == 1
            CisTd = C_val == 4
            if TisTa and CisTd:
                nextMove = DOWN
                return DOWN
            elif C_val > T_val:
                nextMove = RIGHT
                return RIGHT
        if C1 or C0:
            if C1:
                C_val = board[1][1]
            elif C0:
                C_val = board[0][1]
            CisTa = C_val == 1
            CisTd = C_val == 4
            if TisTd and CisTa:
                nextMove = DOWN
                return DOWN
            elif C_val < T_val:
                nextMove = LEFT
                return LEFT
        if nextMove is None or nextMove == oppDirection(lastMove):
            return DOWN
    elif blankx == 3:
        if C2 or C1 or C0:
            if C2:
                C_val = board[2][1]
            elif C1:
                C_val = board[1][1]
            elif C0:
                C_val = board[0][1]
            CisTa = C_val == 1
            CisTd = C_val == 4
            if TisTa and CisTd:
                nextMove = LEFT
                return LEFT
            elif C_val < T_val:
                nextMove = DOWN
                return DOWN
        if nextMove is None or nextMove == oppDirection(lastMove):
            return DOWN


def moveRLDtopRow(blankx, blanky, endTiles, tsInTopRow, tsInBotRow, board, lastMove):
    """Returns nextMove (one of RIGHT, LEFT, DOWN) when one or more tiles are
    in place in the topRow, blanky = topRow, and there is an opportunity to
    pull one of the rowTiles from bottomRow to topRow.  We would like to do
    this without creating a 'reversal'.  This means we may want to shift the
    tsInTopRow to right or left.  Blank is moving toward a target tile that is
    not yet in topRow-bottomRow.  The default direction for blank is DOWN."""

    nextMove = None
    Tax, Tay = endTiles[0][0], endTiles[0][1]
    Tdx, Tdy = endTiles[1][0], endTiles[1][1]
    tsToLeft, tsToRight = getRLTiles(blankx, tsInTopRow, blanky)
    Ta_val, Td_val = board[Tax][Tay], board[Tdx][Tdy]

    if blankx == 0:
        # We have to move down or to the right.  If we move to the right,
        # next decision is made under the blankx == 1 section below.
        topC1 = (1, blanky) in tsToRight
        topC2 = (2, blanky) in tsToRight
        topC3 = (3, blanky) in tsToRight
        botC0 = (0, blanky + 1) in tsInBotRow
        botC1 = (1, blanky + 1) in tsInBotRow
        botC2 = (2, blanky + 1) in tsInBotRow
        # don't bother with tile to far right
#        botC3 = (3, blanky + 1) in tsInBotRow

        if topC1 or topC2 or topC3:
            if topC1:
                tcol = 1
            elif topC2:
                tcol = 2
            elif topC3:
                tcol = 3
            inPlace_val = board[tcol][blanky]
            inPlaceIsTa = inPlace_val == Ta_val
            inPlaceIsTd = inPlace_val == Td_val
            if botC0:
                elem_val = board[0][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if inPlaceIsTa and elemIsTd:
                    nextMove = DOWN
                    return DOWN
                elif not(inPlaceIsTd and elemIsTa):
                    if elem_val < inPlace_val:
                        nextMove = DOWN
                        return DOWN
                    elif lastMove != LEFT:
                        nextMove = RIGHT
                        return RIGHT
                elif lastMove != LEFT:
                    nextMove = RIGHT
                    return RIGHT
            if botC1 or botC2:  # use 'if' here, not elif
                if botC1:
                    column = 1
                elif botC2:
                    column = 2
                elem_val = board[column][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if inPlaceIsTd and elemIsTa:
                    nextMove = RIGHT
                    return RIGHT
                elif not(inPlaceIsTa and elemIsTd):
                    if elem_val > inPlace_val:
                        nextMove = RIGHT
                        return RIGHT  # moves lower-val tile over to left
        if nextMove is None or nextMove == oppDirection(lastMove):
            return DOWN
    elif blankx == 1:
        topC0 = (0, blanky) in tsToLeft
        topC2 = (2, blanky) in tsToRight
        topC3 = (3, blanky) in tsToRight
        botC0 = (0, blanky + 1) in tsInBotRow
        botC1 = (1, blanky + 1) in tsInBotRow
        botC2 = (2, blanky + 1) in tsInBotRow
        botC3 = (3, blanky + 1) in tsInBotRow

        if topC0:
            inPlace_val = board[0][blanky]
            inPlaceIsTa = inPlace_val == Ta_val
            inPlaceIsTd = inPlace_val == Td_val
            if botC0:
                elem_val = board[0][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if inPlaceIsTa and elemIsTd:
                    nextMove = LEFT
                    return LEFT
                elif not(inPlaceIsTd and elemIsTa):
                    if elem_val < inPlace_val:
                        nextMove = LEFT
                        return LEFT
            if botC1:  # again, use 'if' and not elif
                elem_val = board[1][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if inPlaceIsTd and elemIsTa:
                    nextMove = DOWN
                    return DOWN
                elif not(inPlaceIsTa and elemIsTd):
                    if elem_val > inPlace_val:
                        nextMove = DOWN
                        return DOWN
            if botC2:
                elem_val = board[2][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if not topC2:
                    if inPlaceIsTd and elemIsTa:
                        nextMove = RIGHT
                        return RIGHT
                    elif not(inPlaceIsTa and elemIsTd):
                        if elem_val > inPlace_val:
                            nextMove = RIGHT
                            return RIGHT
                elif topC2:  # rowTs in topC0 and topC2
                    topC2_val = board[2][blanky]
                    topC2IsTa = topC2_val == Ta_val
                    topC2IsTd = topC2_val == Td_val
                    if topC2IsTd and elemIsTa:
                        nextMove = RIGHT
                        return RIGHT
                    elif not(topC2IsTa and elemIsTd):
                        if elem_val > topC2_val:
                            nextMove = RIGHT
                            return RIGHT
        if topC2 or topC3:
            if topC2:
                tcol = 2
            elif topC3:
                tcol = 3
            inPlace_val = board[tcol][blanky]
            inPlaceIsTa = inPlace_val == Ta_val
            inPlaceIsTd = inPlace_val == Td_val
            if botC1:
                elem_val = board[1][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if inPlaceIsTa and elemIsTd:
                    nextMove = DOWN
                    return DOWN
                elif not(inPlaceIsTd and elemIsTa):
                    if elem_val < inPlace_val:
                        nextMove = DOWN
                        return DOWN
            if botC2:
                elem_val = board[2][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if inPlaceIsTd and elemIsTa:
                    nextMove = RIGHT
                    return RIGHT
                elif not(inPlaceIsTa and elemIsTd):
                    if elem_val > inPlace_val:
                        nextMove = RIGHT
                        return RIGHT
            if botC3:
                elem_val = board[3][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if not topC3:
                    if inPlaceIsTd and elemIsTa:
                        nextMove = RIGHT
                        return RIGHT
                    elif not(inPlaceIsTa and elemIsTd):
                        if elem_val > inPlace_val:
                            nextMove = RIGHT
                            return RIGHT
                elif topC3:  # rowTs in topC2 and topC3
                    topC3_val = board[3][blanky]
                    topC3IsTa = topC3_val == Ta_val
                    topC3IsTd = topC3_val == Td_val
                    if topC3IsTd and elemIsTa:
                        nextMove = RIGHT
                        return RIGHT
                    elif not(topC3IsTa and elemIsTd):
                        if elem_val > topC3_val:
                            nextMove = RIGHT
                            return RIGHT
        if nextMove is None or nextMove == oppDirection(lastMove):
            return DOWN
    elif blankx == 2:
        topC0 = (0, blanky) in tsToLeft
        topC1 = (1, blanky) in tsToLeft
        topC3 = (3, blanky) in tsToRight
        botC0 = (0, blanky + 1) in tsInBotRow
        botC1 = (1, blanky + 1) in tsInBotRow
        botC2 = (2, blanky + 1) in tsInBotRow
        botC3 = (3, blanky + 1) in tsInBotRow
        # focus on closest tiles first
        if topC1:
            inPlace_val = board[1][blanky]
            inPlaceIsTa = inPlace_val == Ta_val
            inPlaceIsTd = inPlace_val == Td_val
            if botC2:
                elem_val = board[2][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if inPlaceIsTd and elemIsTa:
                    nextMove = DOWN
                    return DOWN
                elif not(inPlaceIsTa and elemIsTd):
                    if elem_val > inPlace_val:
                        nextMove = DOWN
                        return DOWN
            if botC1:
                elem_val = board[1][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if inPlaceIsTa and elemIsTd:
                    nextMove = LEFT
                    return LEFT
                elif not(inPlaceIsTd and elemIsTa):
                    if elem_val < inPlace_val:
                        nextMove = LEFT
                        return LEFT
            if botC3:
                elem_val = board[3][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if not topC3:
                    if inPlaceIsTd and elemIsTa:
                        nextMove = RIGHT
                        return RIGHT
                    elif not(inPlaceIsTa and elemIsTd):
                        if elem_val > inPlace_val:
                            nextMove = RIGHT
                            return RIGHT
                elif topC3:  # rowTs in topC1 and topC3
                    topC3_val = board[3][blanky]
                    topC3IsTa = topC3_val == Ta_val
                    topC3IsTd = topC3_val == Td_val
                    if topC3IsTd and elemIsTa:
                        nextMove = RIGHT
                        return RIGHT
                    elif not(topC3IsTa and elemIsTd):
                        if elem_val > topC3_val:
                            nextMove = RIGHT
                            return RIGHT
        if topC3:
            inPlace_val = board[3][blanky]
            inPlaceIsTa = inPlace_val == Ta_val
            inPlaceIsTd = inPlace_val == Td_val
            if botC2:
                elem_val = board[2][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if inPlaceIsTa and elemIsTd:
                    nextMove = DOWN
                    return DOWN
                elif not(inPlaceIsTd and elemIsTa):
                    if elem_val < inPlace_val:
                        nextMove = DOWN
                        return DOWN
            if botC3:
                elem_val = board[3][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if inPlaceIsTd and elemIsTa:
                    nextMove = RIGHT
                    return RIGHT
                elif not(inPlaceIsTa and elemIsTd):
                    if elem_val > inPlace_val:
                        nextMove = RIGHT
                        return RIGHT
            if botC1:
                elem_val = board[1][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if not topC1:
                    if inPlaceIsTa and elemIsTd:
                        nextMove = LEFT
                        return LEFT
                    elif not(inPlaceIsTd and elemIsTa):
                        if elem_val < inPlace_val:
                            nextMove = LEFT
                            return LEFT
                elif topC1:  # rowTs in topC1 and topC3
                    topC1_val = board[1][blanky]
                    topC1IsTa = topC1_val == Ta_val
                    topC1IsTd = topC1_val == Td_val
                    if topC1IsTa and elemIsTd:
                        nextMove = LEFT
                        return LEFT
                    elif not(topC1IsTd and elemIsTa):
                        if elem_val < topC1_val:
                            nextMove = LEFT
                            return LEFT
        if topC0:
            inPlace_val = board[0][blanky]
            inPlaceIsTa = inPlace_val == Ta_val
            inPlaceIsTd = inPlace_val == Td_val
            if botC2:
                elem_val = board[2][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if inPlaceIsTd and elemIsTa:
                    nextMove = DOWN
                    return DOWN
                elif not(inPlaceIsTa and elemIsTd):
                    if elem_val > inPlace_val:
                        nextMove = DOWN
                        return DOWN
            if botC3:
                elem_val = board[3][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if not topC3:
                    if inPlaceIsTd and elemIsTa:
                        nextMove = RIGHT
                        return RIGHT
                    elif not(inPlaceIsTa and elemIsTd):
                        if elem_val > inPlace_val:
                            nextMove = RIGHT
                            return RIGHT
                elif topC3:  # rowTs in topC0 and topC3
                    topC3_val = board[3][blanky]
                    topC3IsTa = topC3_val == Ta_val
                    topC3IsTd = topC3_val == Td_val
                    if topC3IsTd and elemIsTa:
                        nextMove = RIGHT
                        return RIGHT
                    elif not(topC3IsTa and elemIsTd):
                        if elem_val > topC3_val:
                            nextMove = RIGHT
                            return RIGHT
            if botC1:
                elem_val = board[1][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if not topC1:
                    if inPlaceIsTd and elemIsTa:
                        nextMove = LEFT
                        return LEFT
                    elif not(inPlaceIsTa and elemIsTd):
                        if elem_val > inPlace_val:
                            nextMove = LEFT
                            return LEFT
                elif topC1:  # rowTs in topC0 and topC1
                    topC1_val = board[1][blanky]
                    topC1IsTa = topC1_val == Ta_val
                    topC1IsTd = topC1_val == Td_val
                    if topC1IsTa and elemIsTd:
                        nextMove = LEFT
                        return LEFT
                    elif not(topC1IsTd and elemIsTa):
                        if elem_val < topC1_val:
                            nextMove = LEFT
                            return LEFT
            # do not bother with botC0
        if nextMove is None or nextMove == oppDirection(lastMove):
            return DOWN
    elif blankx == 3:
        topC0 = (0, blanky) in tsToLeft
        topC1 = (1, blanky) in tsToLeft
        topC2 = (2, blanky) in tsToLeft
        botC1 = (1, blanky + 1) in tsInBotRow
        botC2 = (2, blanky + 1) in tsInBotRow
        botC3 = (3, blanky + 1) in tsInBotRow
        # give priority to tiles nearest blank
        if topC2 or topC1 or topC0:
            if topC2:
                tcol = 2
            elif topC1:
                tcol = 1
            elif topC0:
                tcol = 0
            inPlace_val = board[tcol][blanky]
            inPlaceIsTa = inPlace_val == Ta_val
            inPlaceIsTd = inPlace_val == Td_val
            if botC3:
                elem_val = board[3][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if inPlaceIsTd and elemIsTa:
                    nextMove = DOWN
                    return DOWN
                elif not(inPlaceIsTa and elemIsTd):
                    if elem_val > inPlace_val:
                        nextMove = DOWN
                        return DOWN
                    elif lastMove != RIGHT:
                        nextMove = LEFT
                        return LEFT
                elif lastMove != RIGHT:
                    nextMove = LEFT
                    return LEFT
            if botC1 or botC2:  # use 'if' here, not elif
                if botC2:
                    column = 2
                elif botC1:
                    column = 1
                elem_val = board[column][blanky + 1]
                elemIsTa = elem_val == Ta_val
                elemIsTd = elem_val == Td_val
                if inPlaceIsTa and elemIsTd:
                    nextMove = LEFT
                    return LEFT
                elif not(inPlaceIsTd and elemIsTa):
                    if elem_val < inPlace_val:
                        nextMove = LEFT
                        return LEFT  # moves higher-val tile over to right
        if nextMove is None or nextMove == oppDirection(lastMove):
            return DOWN


#############################################################################
### Main functions for getTiles.py
#############################################################################

def getTiles(row, board, lastMove):
    """Returns nextMove (one of UP, DOWN, LEFT, RIGHT) for when we are trying
    to move four row tiles and blank into topRow and bottomRow.  Once the 5
    tiles are retrieved, calls to makeAdjacent4 and order4 can be made.  This
    ftn only gets called when row in ('first', 'second')."""

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

    allRowTs = {(Tax, Tay), (Tbx, Tby), (Tcx, Tcy), (Tdx, Tdy)}
    tsInBotRow = allRowTs & {(0, bottomRow), (1, bottomRow), (2, bottomRow),
                             (3, bottomRow)}
    C0 = (0, bottomRow) in tsInBotRow
    C1 = (1, bottomRow) in tsInBotRow
    C2 = (2, bottomRow) in tsInBotRow
    C3 = (3, bottomRow) in tsInBotRow

    # Identify tiles not in topRow, bottomRow.  The maximum length of displaced
    # will be 5; the minimum length will be 1.
    displaced = getDisplaced(Tay, Tby, Tcy, Tdy, blanky, topRow, bottomRow)
    # displaced is a list of strings; when sorted, 'blank' will be the last
    # element in the list.
    displaced.sort()

    # Since we only need nextMove for this call to getTiles, we do not have to
    # process all elements in the displaced list.  We look only at the first
    # element in the list.
    if len(displaced) == 1 and displaced[0] == 'blank':
        # blank is the only tile that needs to be moved into bottomRow.  This
        # is easy to do as long as we do not have all four rowTiles in the
        # bottomRow.
        if row == 'first' and blanky == 3:
            return UP
        elif (row == 'first' and blanky == 2) or (row == 'second' and blanky == 3):
            if len(tsInBotRow) < 4:
                if blankx == 0:
                    if not C0:
                        return UP
                    else:
                        return RIGHT
                elif blankx == 1:
                    if not C1:
                        return UP
                    elif not C0:
                        return LEFT
                    else:
                        return RIGHT
                elif blankx == 2:
                    if not C2:
                        return UP
                    elif not C3:
                        return RIGHT
                    else:
                        return LEFT
                elif blankx == 3:
                    if not C3:
                        return UP
                    else:
                        return LEFT
            elif len(tsInBotRow) == 4:
                # bubbleUp logic should handle the result of this next move
                return UP
    else:
        target = displaced[0]
        nextMove = bubbleUp(target, row, board, lastMove)
        # A check for infinite loop is done in the calling ftn, getNextMove.
        return nextMove


def bubbleUp(target, row, board, lastMove):
    """Returns nextMove needed to retrieve the target tile and move it into
    the topRow/bottomRow section of the board.  This ftn gets called only when
    row in ('first', 'second').  Because there can be quite a bit of work to do
    before blank gets near the target tile, when blanky in (0, 1) I do not
    directly focus on retrieving the target tile."""

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

    tileDict = {'Ta': (Tax, Tay), 'Tb': (Tbx, Tby), 'Tc': (Tcx, Tcy),
                'Td': (Tdx, Tdy), 'blank': (blankx, blanky), (Tax, Tay): 'Ta',
                (Tbx, Tby): 'Tb', (Tcx, Tcy): 'Tc', (Tdx, Tdy): 'Td',
                (blankx, blanky): 'blank'}

    T = tileDict[target]
    Tx, Ty = T[0], T[1]
    T_val = board[Tx][Ty]
    # identify the other tiles belonging to 'row'
    tmpSet = {(Tax, Tay), (Tbx, Tby), (Tcx, Tcy), (Tdx, Tdy)} - {(Tx, Ty)}
    allRowTs = {(Tax, Tay), (Tbx, Tby), (Tcx, Tcy), (Tdx, Tdy)}
    endTiles = [(Tax, Tay), (Tdx, Tdy)]
    tsInBotRow = tmpSet & {(0, bottomRow), (1, bottomRow), (2, bottomRow),
                           (3, bottomRow)}
    tsInTopRow = tmpSet & {(0, topRow), (1, topRow), (2, topRow), (3, topRow)}
    
    # If all of Ta-Td are displaced, then Ta will be the target tile.  If Ta is
    # in row 3 and Tb-Td are all in row 2 and blank is the fourth tile in row 2,
    # we cannot bring Ta up into row 2 until we move one of Tb-Td up into row 1.
    # To do this, we need to change the target tile.
    rowTsInRow2 = tmpSet & {(0, 2), (1, 2), (2, 2), (3, 2)}
    rowTsInRow3 = tmpSet & {(0, 3), (1, 3), (2, 3), (3, 3)}
    if row == 'first' and len(rowTsInRow2) == 3 and Ty == 3:
        T = tileDict['Td']
        Tx, Ty = T[0], T[1]
        T_val = board[Tx][Ty]
        tmpSet = {(Tax, Tay), (Tbx, Tby), (Tcx, Tcy), (Tdx, Tdy)} - {(Tx, Ty)}

    # Aim is to have blankx == Tx and blanky == Ty - 1.
    if blanky == 0:
        # if blanky == 0, then first row is not done, and so 'row' = 'first',
        # topRow = 0, bottomRow = 1, and the target, T, is in either row 2 or
        # row 3.
        if len(tsInBotRow) == 0:
            return DOWN
        elif len(tsInBotRow) > 0:  # blank is above rowTiles in the bottomRow;
            # move tile in bottomRow with largest value up
            if len(tsInTopRow) == 0:
                highTx = getLargestValCol(tsInBotRow, board, endTiles, rowOfBlank='top')
                # move blank into highTx column (disregarding lastMove);
                # if blankx = highTx, move DOWN
                nextMove = moveRLDefault(blankx, highTx, DOWN)
                return nextMove
            elif len(tsInTopRow) > 0:
                nextMove = moveRLDtopRow(blankx, blanky, endTiles, tsInTopRow,
                                         tsInBotRow, board, lastMove)
                return nextMove
    elif blanky == 1:
        # When row = 'second', we are in topRow.  When row = 'first', we are in
        # bottomRow.
        if row == 'first':
            # if there are rowTs in nextRow, bring one into bottomRow unless
            # there are already 3 rowTs in bottomRow.  If there are already 3
            # rowTs in bottomeRow, we must move one of the tiles up to topRow
            # before proceeding; otherwise we end up with 4 rowTs in bottomRow
            # and blank in row 2 or row 3.
            tsInRow2 = allRowTs & {(0, 2), (1, 2), (2, 2), (3, 2)}

            if len(tsInRow2) == 0:
                if len(tsInBotRow) == 0:  # bottomRow is current row
                    return DOWN
                elif len(tsInBotRow) > 0:
                    if len(tsInBotRow) == 3:
                        # need to ensure we never have 4 rowTs in bottomRow
                        # with blank in row 2 or row3
                        nextMove = UP
                    else:
                        # adjust rowTs in bottomRow before retrieving T in row 3
                        nextMove = moveRLDbotRowAdj(T_val, blankx, blanky,
                                                    tsInBotRow, board, lastMove)
                    return nextMove
            elif len(tsInRow2) > 0:
                highTx = getLargestValCol(tsInRow2, board, endTiles, rowOfBlank='bottom')
                if len(tsInBotRow) == 0:  # bottomRow is current row
                    # Insert highest value rowT in Row2 into bottomRow.
                    nextMove = moveRLDefault(blankx, highTx, DOWN)
                    return nextMove
                elif len(tsInBotRow) > 0:
                    if len(tsInBotRow) == 3:
                        nextMove = UP
                    else:
                        nextMove = moveRLDbotRow(blankx, blanky, highTx, endTiles,
                                                 tsInRow2, tsInBotRow, board, lastMove)
                    return nextMove
        elif row == 'second':
            # blanky is in topRow
            if len(tsInBotRow) == 0:
                return DOWN
            elif len(tsInBotRow) > 0:  # blank is above rowTiles in the bottomRow;
                # move tile in bottomRow with largest value up, if no conflict
                if len(tsInTopRow) == 0:
                    highTx = getLargestValCol(tsInBotRow, board, endTiles, rowOfBlank='top')
                    # move blank into highTx column (disregarding lastMove);
                    # if blankx = highTx, move DOWN
                    nextMove = moveRLDefault(blankx, highTx, DOWN)
                    return nextMove
                elif len(tsInTopRow) > 0:
                    endTiles = [(Tax, Tay), (Tdx, Tdy)]
                    nextMove = moveRLDtopRow(blankx, blanky, endTiles, tsInTopRow,
                                             tsInBotRow, board, lastMove)
                    return nextMove
    elif blanky == 2:
        # Keep in mind that blank could have just moved UP into this row
        # because T was recently pulled into row 2 from row 3
        tsInRow2 = allRowTs & {(0, 2), (1, 2), (2, 2), (3, 2)}
        if row == 'first':
            if (blankx, blanky + 1) in rowTsInRow3 and len(tsInRow2) != 3 and lastMove != UP:
                return DOWN

            if Ty == 3:
                # no need to be concerned here with highTx
                if blankx == Tx:
                    return DOWN
                elif blankx > Tx:
                    return LEFT
                elif blankx < Tx:
                    return RIGHT
            elif Ty == 2:
                C0 = (0, bottomRow) in tsInBotRow
                C1 = (1, bottomRow) in tsInBotRow
                C2 = (2, bottomRow) in tsInBotRow
                C3 = (3, bottomRow) in tsInBotRow

                if lastMove == DOWN:
                    # nextMove cannot be UP.  One reason we might be here: we
                    # just pulled another rowTile up into bottomRow and now
                    # have to move left or right in order to go back up into
                    # bottomRow so that we can pull T into that row.  But when
                    # moving back into bottomRow, we do not want to displace a
                    # rowTile.
                    if blankx == 0:
                        return RIGHT
                    elif blankx == 1:
                        if C0:
                            return RIGHT
                        else:
                            return LEFT
                    elif blankx == 2:
                        if not C3:
                            return RIGHT
                        else:
                            return LEFT
                    elif blankx == 3:
                        return LEFT
                elif lastMove != DOWN:
                    # Case 1: blank and T are in this row because this is the
                    # StartingBoard

                    # Case 2: blank is in this row because there were 2 rowTs
                    # in this row and we recently pulled one of them up into
                    # bottomRow and are now moving toward the next tile.

                    # Case 3: blank is in this row b/c it just came from row 3,
                    # having pulled T into row 2 recently.

                    # In any case, we want blanky = Ty -1 and blankx = Tx. So
                    # we try to move up without displacing a rowTile in row 1.
                    # Because we are in bubbleUp and there is a target tile,
                    # there will always be at least one column in which we can
                    # move up.
                    if blankx == 0:
                        if not C0:
                            return UP
                        else:
                            return RIGHT
                    elif blankx == 1:
                        if not C1:
                            return UP
                        elif not C0:
                            return LEFT
                        else:
                            return RIGHT
                    elif blankx == 2:
                        if not C2:
                            return UP
                        elif not C3:
                            return RIGHT
                        else:
                            return LEFT
                    elif blankx == 3:
                        if not C3:
                            return UP
                        else:
                            return LEFT
        elif row == 'second':
            # blank is in the bottomRow (row 2); target T is in row 3
            tsInRow3 = allRowTs & {(0, 3), (1, 3), (2, 3), (3, 3)}
            
            if len(tsInRow3) == 0:
                pdb.set_trace()
            
            try:
                if len(tsInRow3) == 0:
                    raise ValueError
            except ValueError:
                print("ERROR: (ftn= bubbleUp) Target is supposed to be in row 3.")
            
            highTx = getLargestValCol(tsInRow3, board, endTiles, rowOfBlank='bottom')
            
            if len(tsInBotRow) == 0:
                # Insert highest value rowT in Row3 into bottomRow.
                nextMove = moveRLDefault(blankx, highTx, DOWN)
                return nextMove
            elif len(tsInBotRow) > 0:
                if len(tsInBotRow) == 3:
                    nextMove = UP  # move blank to topRow so that one of the 3
                    # rowTs in bottomRow can be pulled into the topRow
                else:
                    nextMove = moveRLDbotRow(blankx, blanky, highTx, endTiles,
                                             tsInRow3, tsInBotRow, board, lastMove)
                return nextMove
    elif blanky == 3:
        # Want to move UP without displacing rowTiles in row 2.
        tsInRow2 = allRowTs & {(0, 2), (1, 2), (2, 2), (3, 2)}
        if len(tsInRow2) == 0:
            return UP
        elif len(tsInRow2) > 0:
            C0 = (0, 2) in tsInRow2
            C1 = (1, 2) in tsInRow2
            C2 = (2, 2) in tsInRow2
            C3 = (3, 2) in tsInRow2

            if len(tsInRow2) == 4:
                return UP

            if blankx == 0:
                if not C0:
                    return UP
                else:
                    return RIGHT
            elif blankx == 1:
                if not C1:
                    return UP
                elif not C0:
                    return LEFT
                else:
                    return RIGHT
            elif blankx == 2:
                if not C2:
                    return UP
                elif not C3:
                    return RIGHT
                else:
                    return LEFT
            elif blankx == 3:
                if not C3:
                    return UP
                else:
                    return LEFT

#############################################################################
###
#############################################################################
