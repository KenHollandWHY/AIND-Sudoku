# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  

As I understood it, constraint propagation's aim is to limit the amount of options our program can explore. In the sudoku example, we move through the board and eliminate those board positions that are impossible for whatever hueristic we are applying. In eliminate, we cycle through each unit (the collection of 9 boxes that must all have a unique number assigned to them) to make sure that if a single value is already assigned
to a box then that box's peers (all the other boxes in the unit) cannot have that value assigned to them. 
The naked twins strategy extends this idea by realizing that if there are two boxes in a unit containing two identical values, lets say a '12', then one of '1' or '2' will go into one of the two box and the other box will have the other number. Which means that none of the other boxes in the unit, to which the two boxes containing '12' belong, can be allowed to have either a '1' or a '2' in them. The presence of identical twins limits what values the other boxes can be assigned.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: 
In my solution diagonal sudoku is solved by simply adding two new sets of units to the unitlist and thus also to the peers list. And from there the three constraint propogating strategies we have, naked twins,
elimination and only choice go through the updated unitlist and include the two diagonal units I introduced along with the horizontal/vertical and square units and applies the strateigies to them. 
Is this considered a constraint propagation? I suppose we are adding two new units and eliminating some orders that could see the soduku solved in a way that the diagonals contain repeated numbers? So its constraint propagation in the sense that from all the possible solutions we can have, we remove some of the solutions? I would love to get some feedback on how diagonal soduku fits into the constraint propagation rubric. 

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
