from pyamaze import maze, agent, COLOR, textLabel
import time
from classMDP import MarkovDecisionProcessPolicyIteration as mdpPI
from classMDP import MarkovDecisionProcessValueIteration as mdpVI
from classSolver import AStarSearch, DFS, BFS  
from classSolver import MazeCreation

# Class to measure elapsed time
class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = None

    def start(self):
        if self.start_time is not None:
            raise RuntimeError("Stopwatch is already running.")
        self.start_time = time.time()

    def stop(self):
        if self.start_time is None:
            raise RuntimeError("Stopwatch is not running.")
        self.elapsed_time = time.time() - self.start_time
        self.start_time = None

    def reset(self):
        self.start_time = None
        self.elapsed_time = None

# Function to print performance metrics
def printPerformanceMetrics(algorithm, path, elapsedTime, memoryUsage):
    total_steps = len(path) + 1
    print(f'TOTAL STEPS {algorithm}: {total_steps}')
    print(f'TOTAL TIME ELAPSED {algorithm}: {elapsedTime}')
    print(f'TOTAL MEMORY USED {algorithm}: {memoryUsage}\n')

# Main function
if __name__=='__main__':
    # User inputs for maze size and target
    print("\n Enter maze size: \n")
    input_x = input("\n X: ")
    maze_width = int(input_x)
    input_y = input("\n Y: ")
    print("\n Enter Target: \n")
    target_x_input = input("\n X: ")
    target_x = int(target_x_input)
    target_y_input = input("\n Y: ")
    target_y = int(target_y_input)
    print("\n Stochastic? \n")
    stochastic_input = input("\n (y/n) ")
    is_stochastic = stochastic_input == 'y'

    maze_height = int(input_y)
    maze_definition = maze(maze_width, maze_height)
    # Display maze creation options
    print("\nAlgorithm Choice ")
    print("\n 1. BFS")
    print("\n 2. DFS")
    print("\n 3. A Star")
    print("\n 4. MDP PI")
    print("\n 5. MDP VI")
    print("\n 6. BFS Vs DFS")
    print("\n 7. DFS Vs A Star")
    print("\n 8. BFS Vs A Star")
    print("\n 9. BFS Vs DFS Vs A Star")
    print("\n 10. MDP VI Vs MDP PI")
    print("\n 11. All")
    print("\n Type '0' to quit")

    choice = choice = int(input("Enter your choice: "))
    maze_definition = maze(maze_width, maze_height)
    maze_definition.CreateMaze(target_x, target_y, loopPercent=100, theme=COLOR.dark)

    # Perform actions based on user choice
    if(choice==1):
        # BFS Algorithm
        start = time.time()
        bfs_solver = BFS()
        bfs_path, bfs_mem = bfs_solver.solve(maze_definition, (maze_width, maze_height), (target_x, target_y))
        bfs_time_elapsed = time.time() - start

        printPerformanceMetrics('BFS', bfs_path, bfs_time_elapsed,bfs_mem)
        MazeCreation().stepCount(maze_definition, 'BFS', bfs_path)
        MazeCreation().algoTime(maze_definition, 'BFS', bfs_time_elapsed)
        MazeCreation().memoryUsage(maze_definition,'BFS',bfs_mem)
        bfs_agent = MazeCreation().agntMake(maze_definition, 'square', COLOR.red,fill=True)
        maze_definition.tracePath({bfs_agent: bfs_path}, delay=30)
        maze_definition.run()
    elif(choice==2):
        # DFS Algorithm
        start1 = time.time()
        dfs_solver = DFS()
        dfs_path, dfs_mem = dfs_solver.solve(maze_definition, (maze_width, maze_height), (target_x, target_y))
        dfs_time_elapsed = time.time() - start1

        printPerformanceMetrics('DFS', dfs_path, dfs_time_elapsed,dfs_mem)
        MazeCreation().stepCount(maze_definition, 'DFS', dfs_path)
        MazeCreation().algoTime(maze_definition, 'DFS', dfs_time_elapsed)
        MazeCreation().memoryUsage(maze_definition,'DFS',dfs_mem)
        dfs_agent = MazeCreation().agntMake(maze_definition, 'arrow', COLOR.green)
        maze_definition.tracePath({dfs_agent: dfs_path}, delay=30)
        maze_definition.run()
    elif(choice==3):
        # A* Algorithm
        start = time.time()
        astar_solver = AStarSearch()
        astar_path, astar_time_elapsed, astar_mem = astar_solver.aStar(maze_definition, target_x, target_y)
        printPerformanceMetrics('A Star', astar_path, astar_time_elapsed,astar_mem)
        MazeCreation().stepCount(maze_definition, 'A*', astar_path)
        MazeCreation().algoTime(maze_definition, 'A*', astar_time_elapsed)
        MazeCreation().memoryUsage(maze_definition,'A*',astar_mem)
        astar_agent = MazeCreation().agntMake(maze_definition, 'arrow', COLOR.blue)
        maze_definition.tracePath({astar_agent: astar_path}, delay=30)
        maze_definition.run()
    elif(choice==4):
        # MDP Policy Iteration
        pi_path, pi_utilities, pi_policy, pi_time_elapsed,pi_mem = mdpPI().mdp_policyIteration(maze_width, maze_height, target_x, target_y, maze_definition)
        printPerformanceMetrics('MDP PI', pi_path, pi_time_elapsed,pi_mem)
        MazeCreation().stepCount(maze_definition, 'PI', pi_path)
        MazeCreation().algoTime(maze_definition, 'PI', pi_time_elapsed)
        MazeCreation().memoryUsage(maze_definition,'PI',pi_mem)
        pi_agent = MazeCreation().agntMake(maze_definition, 'square', COLOR.yellow, fill=True)
        maze_definition.tracePath({pi_agent: pi_path}, delay=30)
        maze_definition.run()
    elif(choice==5):
        # MDP Value Iteration
        vi_instance = mdpVI()
        vi_instance.mdpVIInit(target_x, target_y, -4, 0.8, 10**(-3))
        vi_instance.stochastic = is_stochastic
        vi_path, vi_utilities, vi_policy, vi_actions, vi_time_elapsed,vi_mem = vi_instance.Tracking_Maze((maze_width, maze_height), maze_definition)
        printPerformanceMetrics('MDP VI', vi_path, vi_time_elapsed,vi_mem)
        MazeCreation().stepCount(maze_definition, 'VI', vi_path)
        MazeCreation().algoTime(maze_definition, 'VI', vi_time_elapsed)
        MazeCreation().memoryUsage(maze_definition,'VI',vi_mem)
        vi_agent = MazeCreation().agntMake(maze_definition, 'square', COLOR.cyan, fill=True)
        maze_definition.tracePath({vi_agent: vi_path}, delay=30)
        maze_definition.run()
        
    elif(choice==6):
        # BFS vs DFS Comparison
        start1 = time.time()
        dfs_solver = DFS()
        dfs_path, dfs_mem = dfs_solver.solve(maze_definition, (maze_width, maze_height), (target_x, target_y))
        dfs_time_elapsed = time.time() - start1

        start = time.time()
        bfs_solver = BFS()
        bfs_path, bfs_mem = bfs_solver.solve(maze_definition, (maze_width, maze_height), (target_x, target_y))
        bfs_time_elapsed = time.time() - start
        
        printPerformanceMetrics('BFS', bfs_path, bfs_time_elapsed,bfs_mem)
        printPerformanceMetrics('DFS', dfs_path, dfs_time_elapsed,dfs_mem)
        
        
        MazeCreation().stepCount(maze_definition, 'DFS', dfs_path)
        MazeCreation().algoTime(maze_definition, 'DFS', dfs_time_elapsed)
        MazeCreation().memoryUsage(maze_definition,'DFS',dfs_mem)
        
        MazeCreation().stepCount(maze_definition, 'BFS', bfs_path)
        MazeCreation().algoTime(maze_definition, 'BFS', bfs_time_elapsed)
        MazeCreation().memoryUsage(maze_definition,'BFS',bfs_mem)
    
        
        dfs_agent = MazeCreation().agntMake(maze_definition, 'arrow', COLOR.green)
        bfs_agent = MazeCreation().agntMake(maze_definition, 'square', COLOR.red,fill=True)        

        maze_definition.tracePath({dfs_agent: dfs_path}, delay=30)
        maze_definition.tracePath({bfs_agent: bfs_path}, delay=30)
        maze_definition.run()
    elif(choice==7): 
        # DFS vs A* Comparison
        start1 = time.time()
        dfs_solver = DFS()
        dfs_path, dfs_mem = dfs_solver.solve(maze_definition, (maze_width, maze_height), (target_x, target_y))
        dfs_time_elapsed = time.time() - start1

        start = time.time()
        astar_solver = AStarSearch()
        astar_path, astar_time_elapsed, astar_mem = astar_solver.aStar(maze_definition, target_x, target_y)        
        printPerformanceMetrics('A Star', astar_path, astar_time_elapsed,astar_mem)
        printPerformanceMetrics('DFS', dfs_path, dfs_time_elapsed,dfs_mem)
        
        
        MazeCreation().stepCount(maze_definition, 'DFS', dfs_path)
        MazeCreation().algoTime(maze_definition, 'DFS', dfs_time_elapsed)
        MazeCreation().memoryUsage(maze_definition,'DFS',dfs_mem)
        
        
        MazeCreation().stepCount(maze_definition, 'A*', astar_path)
        MazeCreation().algoTime(maze_definition, 'A*', astar_time_elapsed)
        MazeCreation().memoryUsage(maze_definition,'A*',astar_mem)
                
        dfs_agent = MazeCreation().agntMake(maze_definition, 'arrow', COLOR.green)
        
        astar_agent = MazeCreation().agntMake(maze_definition, 'square', COLOR.blue,fill=True)
        
        maze_definition.tracePath({dfs_agent: dfs_path}, delay=30)
        maze_definition.tracePath({astar_agent: astar_path}, delay=30)
        maze_definition.run()
    elif(choice==8):
        # BFS vs A* Comparison
        start = time.time()
        bfs_solver = BFS()
        bfs_path, bfs_mem = bfs_solver.solve(maze_definition, (maze_width, maze_height), (target_x, target_y))
        bfs_time_elapsed = time.time() - start

        start = time.time()
        astar_solver = AStarSearch()
        astar_path, astar_time_elapsed, astar_mem = astar_solver.aStar(maze_definition, target_x, target_y)
        
        printPerformanceMetrics('A Star', astar_path, astar_time_elapsed,astar_mem)
        printPerformanceMetrics('BFS', bfs_path, bfs_time_elapsed,bfs_mem)
    
        
        
        MazeCreation().stepCount(maze_definition, 'BFS', bfs_path)
        MazeCreation().algoTime(maze_definition, 'BFS', bfs_time_elapsed)
        MazeCreation().memoryUsage(maze_definition,'BFS',bfs_mem)
        
        MazeCreation().stepCount(maze_definition, 'A*', astar_path)
        MazeCreation().algoTime(maze_definition, 'A*', astar_time_elapsed)
        MazeCreation().memoryUsage(maze_definition,'A*',astar_mem)
        

        
        bfs_agent = MazeCreation().agntMake(maze_definition, 'square', COLOR.red,fill=True)
        astar_agent = MazeCreation().agntMake(maze_definition, 'arrow', COLOR.blue)
        
        maze_definition.tracePath({bfs_agent: bfs_path}, delay=30)
        maze_definition.tracePath({astar_agent: astar_path}, delay=30)
        maze_definition.run()
    elif(choice==9):
        # BFS vs DFS vs A* Comparison
        start = time.time()
        bfs_solver = BFS()
        bfs_path, bfs_mem = bfs_solver.solve(maze_definition, (maze_width, maze_height), (target_x, target_y))
        bfs_time_elapsed = time.time() - start
        
        start = time.time()
        astar_solver = AStarSearch()
        astar_path, astar_time_elapsed, astar_mem = astar_solver.aStar(maze_definition, target_x, target_y)
        
        start1 = time.time()
        dfs_solver = DFS()
        dfs_path, dfs_mem = dfs_solver.solve(maze_definition, (maze_width, maze_height), (target_x, target_y))
        dfs_time_elapsed = time.time() - start1
       
        printPerformanceMetrics('A Star', astar_path, astar_time_elapsed,astar_mem)
        printPerformanceMetrics('BFS', bfs_path, bfs_time_elapsed,bfs_mem)
        printPerformanceMetrics('DFS', dfs_path, dfs_time_elapsed,dfs_mem)
  
        MazeCreation().stepCount(maze_definition, 'BFS', bfs_path)
        MazeCreation().algoTime(maze_definition, 'BFS', bfs_time_elapsed)
        MazeCreation().memoryUsage(maze_definition,'BFS',bfs_mem)
        
        MazeCreation().stepCount(maze_definition, 'A*', astar_path)
        MazeCreation().algoTime(maze_definition, 'A*', astar_time_elapsed)
        MazeCreation().memoryUsage(maze_definition,'A*',astar_mem)
        
        MazeCreation().stepCount(maze_definition, 'DFS', dfs_path)
        MazeCreation().algoTime(maze_definition, 'DFS', dfs_time_elapsed)
        MazeCreation().memoryUsage(maze_definition,'DFS',dfs_mem)
        
        
        bfs_agent = MazeCreation().agntMake(maze_definition, 'square', COLOR.red,fill=True)
        astar_agent = MazeCreation().agntMake(maze_definition, 'arrow', COLOR.blue)
        dfs_agent = MazeCreation().agntMake(maze_definition, 'arrow', COLOR.green)

     
        
        maze_definition.tracePath({bfs_agent: bfs_path}, delay=30)
        maze_definition.tracePath({astar_agent: astar_path}, delay=30)
        maze_definition.tracePath({dfs_agent: dfs_path}, delay=30)
        maze_definition.run()
    elif(choice==10):
        # MDP VI vs MDP PI Comparison
        vi_instance = mdpVI()
        vi_instance.mdpVIInit(target_x, target_y, -4, 0.8, 10**(-3))
        vi_instance.stochastic = is_stochastic
        vi_path, vi_utilities, vi_policy, vi_actions, vi_time_elapsed,vi_mem = vi_instance.Tracking_Maze((maze_width, maze_height), maze_definition)

        pi_path, pi_utilities, pi_policy, pi_time_elapsed,pi_mem = mdpPI().mdp_policyIteration(maze_width, maze_height, target_x, target_y, maze_definition)
        
        
        printPerformanceMetrics('MDP VI', vi_path, vi_time_elapsed,vi_mem)
        printPerformanceMetrics('MDP PI', pi_path, pi_time_elapsed,pi_mem)
        
        
        MazeCreation().stepCount(maze_definition, 'VI', vi_path)
        MazeCreation().algoTime(maze_definition, 'VI', vi_time_elapsed)
        MazeCreation().memoryUsage(maze_definition,'VI',vi_mem)
        
        MazeCreation().stepCount(maze_definition, 'PI', pi_path)
        MazeCreation().algoTime(maze_definition, 'PI', pi_time_elapsed)
        MazeCreation().memoryUsage(maze_definition,'PI',pi_mem)
        
        vi_agent = MazeCreation().agntMake(maze_definition, 'square', COLOR.cyan, fill=True)
        pi_agent = MazeCreation().agntMake(maze_definition, 'square', COLOR.yellow, fill=True)
        

        maze_definition.tracePath({vi_agent: vi_path}, delay=30)
        maze_definition.tracePath({pi_agent: pi_path}, delay=30)
        maze_definition.run()

    elif(choice==11):
        # All Algorithms
        vi_instance = mdpVI()
        vi_instance.mdpVIInit(target_x, target_y, -4, 0.8, 10**(-3))
        vi_instance.stochastic = is_stochastic
        vi_path, vi_utilities, vi_policy, vi_actions, vi_time_elapsed,vi_mem = vi_instance.Tracking_Maze((maze_width, maze_height), maze_definition)

        pi_path, pi_utilities, pi_policy, pi_time_elapsed,pi_mem = mdpPI().mdp_policyIteration(maze_width, maze_height, target_x, target_y, maze_definition)
        
        start1 = time.time()
        dfs_solver = DFS()
        dfs_path, dfs_mem = dfs_solver.solve(maze_definition, (maze_width, maze_height), (target_x, target_y))
        dfs_time_elapsed = time.time() - start1

        start = time.time()
        bfs_solver = BFS()
        bfs_path, bfs_mem = bfs_solver.solve(maze_definition, (maze_width, maze_height), (target_x, target_y))
        bfs_time_elapsed = time.time() - start

        start = time.time()
        astar_solver = AStarSearch()
        astar_path, astar_time_elapsed, astar_mem = astar_solver.aStar(maze_definition, target_x, target_y)


        
        printPerformanceMetrics('MDP VI', vi_path, vi_time_elapsed,vi_mem)
        printPerformanceMetrics('MDP PI', pi_path, pi_time_elapsed,pi_mem)
        printPerformanceMetrics('A Star', astar_path, astar_time_elapsed,astar_mem)
        printPerformanceMetrics('BFS', bfs_path, bfs_time_elapsed,bfs_mem)
        printPerformanceMetrics('DFS', dfs_path, dfs_time_elapsed,dfs_mem)
        
        
        MazeCreation().stepCount(maze_definition, 'DFS', dfs_path)
        MazeCreation().algoTime(maze_definition, 'DFS', dfs_time_elapsed)
        MazeCreation().memoryUsage(maze_definition,'DFS',dfs_mem)
        
        MazeCreation().stepCount(maze_definition, 'BFS', bfs_path)
        MazeCreation().algoTime(maze_definition, 'BFS', bfs_time_elapsed)
        MazeCreation().memoryUsage(maze_definition,'BFS',bfs_mem)
        
        MazeCreation().stepCount(maze_definition, 'A*', astar_path)
        MazeCreation().algoTime(maze_definition, 'A*', astar_time_elapsed)
        MazeCreation().memoryUsage(maze_definition,'A*',astar_mem)
        
        MazeCreation().stepCount(maze_definition, 'VI', vi_path)
        MazeCreation().algoTime(maze_definition, 'VI', vi_time_elapsed)
        MazeCreation().memoryUsage(maze_definition,'VI',vi_mem)
        
        MazeCreation().stepCount(maze_definition, 'PI', pi_path)
        MazeCreation().algoTime(maze_definition, 'PI', pi_time_elapsed)
        MazeCreation().memoryUsage(maze_definition,'PI',pi_mem)
        
        dfs_agent = MazeCreation().agntMake(maze_definition, 'arrow', COLOR.green)
        bfs_agent = MazeCreation().agntMake(maze_definition, 'square', COLOR.red,fill=True)
        astar_agent = MazeCreation().agntMake(maze_definition, 'arrow', COLOR.blue)
        vi_agent = MazeCreation().agntMake(maze_definition, 'square', COLOR.yellow, fill=False)
        pi_agent = MazeCreation().agntMake(maze_definition, 'square', COLOR.cyan, fill=True)
        
        
        maze_definition.tracePath({vi_agent: vi_path}, delay=20)
        maze_definition.tracePath({pi_agent: pi_path}, delay=20)
        maze_definition.tracePath({dfs_agent: dfs_path}, delay=20)
        maze_definition.tracePath({bfs_agent: bfs_path}, delay=20)
        maze_definition.tracePath({astar_agent: astar_path}, delay=20)
        maze_definition.run()
    else:
        print("Invalid Choice")
