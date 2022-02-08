init_state = input()

class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier:
    remove_from = -1

    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def empty(self):
        return len(self.frontier) == 0

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def remove(self):
        if self.empty():
            raise Exception('Empty frontier')
        else:
            return self.frontier.pop(remove_from)

class QueueFrontier(StackFrontier):
    remove_from = 0

class Maze:
    def __init__(self, filename):
        with open(filename) as f:
            maze = f.read()

        # find height and width of the maze
        maze = maze.split('\n')
        self.height = len(maze)
        self.width = max(len(line) for line in maze)

        # recognize walls
        
