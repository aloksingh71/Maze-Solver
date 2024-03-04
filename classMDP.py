from queue import PriorityQueue
import random
import time
import psutil
GLOBAL_VISITED = []



def mazeTrace(mazeDef, currentNode, direction):
    if direction == 'E':
        return (currentNode[0], currentNode[1]+1)
    elif direction == 'W':
        return (currentNode[0], currentNode[1]-1)
    elif direction == 'N':
        return (currentNode[0]-1, currentNode[1])
    elif direction == 'S':
        return (currentNode[0]+1, currentNode[1])

class MarkovDecisionProcessValueIteration():
    """
    Class to implement the Markov Decision Process for Value Iteration.
    """
    def __init__(self):
        self.REWARD = None
        self.DISCOUNT = None
        self.MAX_ERROR = None
        self.ACTIONS = {}
        self.U = None
        self.target = []
        self.policy = {}
        self.tracePath = {}
        self.algoPath = {}
        self.stochastic = None

    def mdpVIInit(self, xTarget, yTarget, reward, gamma, error):
        """
        Initializes the MDP Value Iteration with target, reward, discount factor, and maximum error.
        """
        self.REWARD = reward
        self.DISCOUNT = gamma
        self.MAX_ERROR = error
        self.target = [(xTarget, yTarget)]
        return self.REWARD, self.DISCOUNT, self.MAX_ERROR, self.target

    def mdpVIActions(self, mazeDef):
        """
        Initializes the actions and utilities for each state based on the maze definition.
        """
        for key, val in mazeDef.maze_map.items():
            self.ACTIONS[key] = [(k, v) for k, v in val.items() if v == 1]

        for k, v in self.ACTIONS.items():
            self.ACTIONS[k] = dict(v)
        
        if self.stochastic:
            for key, val in self.ACTIONS.items():
                for k, v in val.items():
                    if k == 'N':
                        val[k] = 0.80
                    elif k == 'W':
                        val[k] = 0.1
                    elif k == 'E':
                        val[k] = 0.05
                    elif k == 'S':
                        val[k] = 0.05
        else:
            for key, val in self.ACTIONS.items():
                for k, v in val.items():
                    val[k] = 1
                
        self.U = {state: 0 for state in self.ACTIONS.keys()}
        self.U[self.target[0]] = 1
        
        return self.ACTIONS, self.U


    
    def mdpValIter(self, mazeDef):
        """
        Performs the Value Iteration algorithm.
        """
        while True:
            delta = 0
            for state in self.ACTIONS.keys():
                if state == self.target[0]:
                    continue
                max_utility = float("-infinity")
                max_action = None
                for action, prob in self.ACTIONS[state].items():
                    for direction in action:
                        if mazeDef.maze_map[state][direction]==True:  
                            next_state = mazeTrace(mazeDef, state, direction)
                    utility = 0
                    reward = self.REWARD
                    if next_state == self.target[0]:
                        reward = 100000
                    utility = reward + self.DISCOUNT*(prob*self.U[next_state])
                    if utility > max_utility:
                        max_utility = utility
                        max_action = action
                delta = max(delta, abs(max_utility - self.U[state]))
                self.U[state] = max_utility
                self.policy[state] = max_action
            if delta < self.MAX_ERROR:
                break
            return self.U, self.policy, self.ACTIONS
            
    def Tracking_Maze(self, currNode, mazeDef):
        """
        Tracks the path from the current node to the target using the calculated policy.
        """
        start = time.time()
        start_mem = psutil.Process().memory_info().rss
        self.ACTIONS, self.U = self.mdpVIActions(mazeDef)
        self.mdpValIter(mazeDef)
        node = currNode
        while True:
            bestNode = None
            bestNodeVal = None
            if node == self.target[0]:
                break
            for direction in 'NWSE':
                if mazeDef.maze_map.get(node, {}).get(direction, False) and mazeTrace(mazeDef, node, direction) not in GLOBAL_VISITED:
                    directionalNode =  mazeTrace(mazeDef, node, direction)
                    if  directionalNode == self.target[0]:
                        bestNode =  directionalNode
                        bestNodeVal = self.U[bestNode]
                        break
                    if bestNodeVal == None:
                        bestNode = directionalNode
                        bestNodeVal = self.U[bestNode]
                    else:
                        tempNode = directionalNode
                        if bestNodeVal < self.U[tempNode]:
                            bestNode = tempNode
                            bestNodeVal = self.U[tempNode]
            GLOBAL_VISITED.append(bestNode)
            self.tracePath[node] = bestNode
            node = bestNode
            end = time.time()
            end_mem = psutil.Process().memory_info().rss
        return self.tracePath, self.U, self.policy, self.ACTIONS, (end-start),(end_mem-start_mem)

class MarkovDecisionProcessPolicyIteration():
    """
    Class to implement the Markov Decision Process for Policy Iteration.
    """
    def mdp_policyIteration(self, initialX, initialY, targerx, tary, mazeDef):
        """
        Performs the Policy Iteration algorithm.
        """
        start_mem = psutil.Process().memory_info().rss
        start = time.time()
        target = [(targerx, tary)]
        actions = {}
        for key, val in mazeDef.maze_map.items():
            actions[key] = [(k, v) for k, v in val.items() if v == 1]

        for k, v in actions.items():
            actions[k] = dict(v)

        U = {state: 0 for state in actions.keys()}
        U[target[0]] = 10**(8)
        policy = {s: random.choice('NSEW') for s in actions.keys()}
        
        REWARD = {state: -40 for state in actions.keys()}
        REWARD[target[0]] = 10**(8)
        DISCOUNT = 0.9
        is_policy_changed = True
        iterations = 0
        
        while is_policy_changed:
            is_policy_changed = False
            is_value_changed = True
            while is_value_changed:
                is_value_changed = False
                for state in actions.keys():
                    if state == target[0]:
                        continue
                    max_utility = float("-infinity")
                    max_action = None
                    for action, prob in actions[state].items():
                        for direction in action:
                            if mazeDef.maze_map[state][direction]==True:  
                                next_state = mazeTrace(mazeDef, state, direction)
                        reward = REWARD[state]
                        if next_state == target[0]:
                            reward = 10**(7)
                        utility = reward + DISCOUNT*(prob*U[next_state])
                        if utility > max_utility:
                            max_utility = utility
                            max_action = action
                        policy[state] = max_action
                        U[state] = max_utility
                        if policy[state] != max_action:
                            is_policy_changed = True
                            policy[state] = max_action
                    iterations += 1
        currNode = (initialX,initialY)   
        tracePath = {}
        while currNode != target[0]:
            test = mazeTrace(mazeDef, currNode, policy[currNode])
            tracePath[currNode] = test
            currNode = test
        end = time.time()
        end_mem = psutil.Process().memory_info().rss
        return tracePath, U, policy, (end-start),(end_mem-start_mem)
