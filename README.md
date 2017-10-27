# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Constraint Propagation is a general Sudoko strategy of using local constraints to eliminate possibilities from a
search space for the solution to a puzzle or problem. In the case of Naked Twins, we use the constraint that within a
given Sudoku unit only one box may contain one of the digits 1-9. If two boxes within a given unit have the same two
remaining digits remaining (because boxes in other units that belong to 'claimed' the other digits), then the boxes are
"Naked Twins". Because of the original constraint that a unit can only have a digit once and the fact that the two
digits must belong to the twins (as they have no options), we can propagate the constraint to eliminate the two digits
from other boxes with in the unit. This thus reduces the search space.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: For the Diagonal Sudoku problem, we use three methods of constraint propagation. First, we apply the only one
strategy in which if a unit has a box (or boxes) that has been solved (the value has been set), we can use the
constraint that a digit can only occur once within a unit to allow us to eliminate the individual digits that have been
set from the remaining digits available to the other boxes within in the unit. Second, we use the only choice strategy,
which uses the logical argument that if there is only one box with in a unit that would allow a certain value, then that
box must be assigned that digit. Finally, we also apply Naked Twins as above.

By applying these constraints iteratively in conjunction with depth first search, we are able to solve almost any
standard Sudoku puzzle. To solve the Diagonal Sudoku problem specifically, we add two additional constraints to the
puzzle by adding the diagonal units, meaning that the diagonals too must contain each digit once.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - Fill in the required functions in this file to complete the project.
* `test_solution.py` - You can test your solution by running `python -m unittest`.
* `PySudoku.py` - This is code for visualizing your solution.
* `visualize.py` - This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

