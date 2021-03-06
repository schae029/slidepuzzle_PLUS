# slidepuzzle_PLUS
Slide puzzle game with scoring and the ability to play against the computer.

This set of programs is an enhancement of Al Sweigart's Slide Puzzle program.  See http://inventwithpython.com/pygame and Chapter 4 (Slide Puzzle) of Sweigart's book, "Making Games with Python and Pygame" (2012).

I have made 2 major enhancements to Sweigart's game: 

  (a) I added a scoring algorithm which counts the number of clicks the user needs to solve the puzzle and which keeps track of the time it takes the user to solve the puzzle.  The user's final score is the sum of the number of clicks used and the number of seconds used, IF the user solved the puzzle in the allotted TIMEPERGAME.  If the user did not solve the puzzle in the allotted time, a penalty is added to their score (a penalty based on my experience playing the game).  If the computer algorithm is used to play the game, the final score counts only the number of clicks needed to solve the puzzle.  Thus, if a user wants to play against the computer, they should compare their number of clicks, assuming they have solved the puzzle, with the number of clicks needed by the algorithm.  When playing against the computer, the user should go first and, when finished, hit the RESET button; this will return the board to the same puzzle the user just solved, or tried to solve.  The user can then apply the algorithm to the very same puzzle to see how their effort compares with what the algorithm does.
  
  (b) I added the ability for the computer to play the game, i.e., for the puzzle to be solved by an algorithm.  This is done by clicking on the button, Compute Move, until the puzzle is solved.  Since the algorithm is not as optimized as it could be, the user has a decent chance of beating it on a subset of the puzzles presented.  This should make the game interesting when the user is playing against the computer.
  
At some point in the future I expect to further enhance the game, allowing the user to enter the number of players playing, their names, and to set the desired playing level.  The different playing levels will be distinguished by the allotted time per game.  At the moment, the program allows the user 160 seconds to solve the puzzle.  You will see that 130 seconds is probably a more appropriate amount of time when playing against another person, rather than against the computer algorithm.  But when challenging the algorithm, it helps to have some extra time to complete the puzzle. 
  
The code for the slide puzzle algorithm is robust in the sense that it has successfully handled over 1.5 million randomly generated puzzles.  See the spPLUS_TESTING_module.py file for the code I used to test large numbers of boards at once.  When the random puzzle generation function used 130 moves to randomize the board 200K times, my algorithm needed, on average, 145.1 moves to arrive at the solved state.  The standard deviation was 31.13 moves.  The frequency distribution for moves needed is a normal distribution, or very close to it.
  
While the algorithm is robust, it may not be perfect in the sense that it can solve all boards presented to it.  There are almost 21 trillion permutations for the 16 tiles, half of which can be slide puzzle puzzles.  Thus, I have tested my algorithm against only a small fraction of the possible puzzles.


Final note: when challenging the algorithm, it is best to play around 20 games against it and look at the total games won out of total games played.  Have fun.

