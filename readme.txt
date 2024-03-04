
README.txt for Project

Welcome to our Maze Solving Project! This project implements various algorithms to solve mazes, including Breadth-First Search (BFS), Depth-First Search (DFS), A*, Markov Decision Process (MDP) Value Iteration, and MDP Policy Iteration. Below are the command lines to run each algorithm through our main entry point `main.py`.

### Prerequisites

- Python 3.x
- pyamaze library
- psutil library

### Running the Project

1. **General Setup**:
   - Ensure Python 3.x is installed on your system.
   - Install required Python packages: `pyamaze` and `psutil`.

2. **Executing Algorithms**:
   - Navigate to the project directory.
   - Run `main.py` using Python and follow the on-screen prompts to select the algorithm and maze parameters.
   
   Command Line:
   ```
   python main.py
   ```

   You will be prompted to:
   - Enter maze size (width and height).
   - Specify the target location within the maze.
   - Choose whether the maze should be stochastic or not.
   - Select the algorithm to solve the maze by entering the corresponding number:
     - 1 for BFS
     - 2 for DFS
     - 3 for A Star
     - 4 for MDP Policy Iteration
     - 5 for MDP Value Iteration
     - 6 to run all algorithms sequentially
     - Type '0' to quit

   Follow the prompts to complete the execution.

### Files Overview

- `classMDP.py`: Implements the MDP Value Iteration and Policy Iteration algorithms.
- `classSolver.py`: Contains the A*, BFS, and DFS algorithms, along with utility functions for maze creation and manipulation.
- `main.py`: The main script to run the project, integrating all algorithms and providing a user interface to interact with the system.

For more detailed information about each algorithm and how they are implemented, refer to the comments and documentation within each `.py` file.


## TO EXECUTE RUN Python main.py  in the directory in which the main.py is located

