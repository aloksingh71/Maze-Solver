from pyamaze import maze, agent, COLOR, textLabel
from queue import PriorityQueue
import time
import psutil

class MazeCreation:
    """
    Class to handle maze creation and visualization.
    """
    def agntMake(self, mazeDef, traceShape, traceColor, fill=False):
        """
        Creates an agent in the maze with specified properties.
        """
        agnt = agent(mazeDef, footprints=True, shape=traceShape, color=traceColor, filled=fill)
        return agnt
    
    def stepCount(self, mazeDef, name, algo):
        """
        Creates a label to display the step count.
        """
        stepLabel = textLabel(mazeDef, f'{name} Steps: ', len(algo) + 1)
        return stepLabel

    def algoTime(self, mazeDef, name, delta):
        """
        Creates a label to display the time taken by the algorithm.
        """
        if isinstance(delta, (int, float)):
            stepLabelT = textLabel(mazeDef, f'{name} Time: ', round(delta, 3))
        else:
            stepLabelT = None  
        return stepLabelT
    
    def memoryUsage(self, mazeDef, name, mem_usage):
        """
        Creates a label to display the memory usage of the algorithm.
        """
        mem_usage1 = mem_usage / 1024 / 1024  # Memory usage in MB
        mem_label = textLabel(mazeDef, f'{name} Memory: ', round(mem_usage1, 3))
        return mem_label

class SearchAlgorithms:
    """
    Class containing different search algorithms for solving mazes.
    """
    def mazeTrace(self, mazeDef, currentNode, direction):     
        """
        Calculates the next node in the maze based on the current node and direction.
        """
        if direction == 'E':
            return (currentNode[0], currentNode[1] + 1)
        elif direction == 'W':
            return (currentNode[0], currentNode[1] - 1)
        elif direction == 'N':
            return (currentNode[0] - 1, currentNode[1])
        elif direction == 'S':
            return (currentNode[0] + 1, currentNode[1])

class DFS:
    """
    Depth-First Search algorithm for solving mazes.
    """
    def solve(self, mazeDef, startNode, target):
        """
        Solves the maze using Depth-First Search algorithm.
        """
        start_mem = psutil.Process().memory_info().rss
        stack = [(startNode, [])]
        visited = set()
        final_path = None
        while stack:
            node, path = stack.pop()
            if node == target:
                final_path = path + [node]
                continue
            if node in visited:
                continue
            visited.add(node)
            for direction in 'NSEW':
                if mazeDef.maze_map[node][direction]:
                    next_node = SearchAlgorithms().mazeTrace(mazeDef, node, direction)
                    stack.append((next_node, path + [node]))
        end_mem = psutil.Process().memory_info().rss
        return final_path if final_path else [], (end_mem - start_mem)

class BFS:
    """
    Breadth-First Search algorithm for solving mazes.
    """
    def solve(self, mazeDef, startNode, target):
        """
        Solves the maze using Breadth-First Search algorithm.
        """
        start_mem = psutil.Process().memory_info().rss
        queue = [(startNode, [])]
        visited = set()
        while queue:
            node, path = queue.pop(0)
            if node == target:
                end_mem = psutil.Process().memory_info().rss
                return path + [node], (end_mem - start_mem)
            if node in visited:
                continue
            visited.add(node)
            for direction in 'NSEW':
                if mazeDef.maze_map[node][direction]:
                    next_node = SearchAlgorithms().mazeTrace(mazeDef, node, direction)
                    queue.append((next_node, path + [node]))
        end_mem = psutil.Process().memory_info().rss
        return [], (end_mem - start_mem)

class AStarSearch:
    """
    Class containing A* search algorithm for solving mazes.
    """
    def calNodeCost(self, node1, node2):
        """
        Calculates the cost between two nodes.
        """
        x1, y1 = node1
        x2, y2 = node2
        return abs(x1 - x2) + abs(y1 - y2)
    
    def aStarInit(self, mazeDef, xtarget, ytarget):
        """
        Initializes A* search with required parameters.
        """
        startNode = (mazeDef.rows, mazeDef.cols)
        nodeDist = {node: float('inf') for node in mazeDef.grid}
        totalNodeCost = {node: float('inf') for node in mazeDef.grid}
        return startNode, nodeDist, totalNodeCost 

    def aStar(self, mazeDef, xtarget, ytarget):
        """
        Solves the maze using A* search algorithm.
        """
        start = time.time()
        start_mem = psutil.Process().memory_info().rss
        startNode, nodeDist, totalNodeCost = self.aStarInit(mazeDef, xtarget, ytarget)
        nodeDist[startNode] = 0
        totalNodeCost[startNode] = self.calNodeCost(startNode, (xtarget, ytarget))
        algoPath = {}
        tracePath = {}
        nextNode = None
        tempNodeDist = None
        tempTotalNodeCost = None
        currentNode = None
        cell = (xtarget, ytarget)
        container = PriorityQueue()
        container.put((totalNodeCost[startNode], startNode))
        search_algorithms = SearchAlgorithms()
        while not container.empty():
            currentNode = container.get()[1]
            
            if currentNode == (xtarget, ytarget):
                break
            
            for direction in 'NSEW':
                if mazeDef.maze_map[currentNode][direction]:
                    nextNode = search_algorithms.mazeTrace(mazeDef, currentNode, direction)

                    tempNodeDist = nodeDist[currentNode] + 1
                    tempTotalNodeCost = tempNodeDist + self.calNodeCost(nextNode, (xtarget, ytarget))
                    
                    if tempTotalNodeCost < totalNodeCost[nextNode]:
                        nodeDist[nextNode] = tempNodeDist
                        totalNodeCost[nextNode] = tempTotalNodeCost
                        container.put((tempTotalNodeCost, nextNode))
                        algoPath[nextNode] = currentNode
       
        while cell != startNode:
            tracePath[algoPath[cell]] = cell
            cell = algoPath[cell]
        
        end = time.time()
        end_mem = psutil.Process().memory_info().rss
        return tracePath, (end - start), (end_mem - start_mem)
