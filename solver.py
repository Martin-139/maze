import creator
import random, os, sys, time

start = 'A'
end = 'B'
wall = '[]'
maze = None

def print_maze(maze):
    if os.name == 'nt':
        os.system('cls')
    for r in maze:
        for b in r:
            if b == wall:
                print('\u001b[47m  \u001b[40m', end='') # (background colors)
            elif b == start or b == end:
                print('\u001b[44m  \u001b[40m', end='')
            elif b == '*':
                print('\u001b[41m  \u001b[40m', end='')
            else:
                print('\u001b[40m  ', end='')
        print()

class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

# removes elements from the top (LIFO)
class StackFrontier:
    def __init__(self):
        self.frontier = []
        self.remove_from = -1

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
            return self.frontier.pop(self.remove_from)
# removes elements from the bottom (FIFO)
class QueueFrontier(StackFrontier):
    def __init__(self):
        self.frontier = []
        self.remove_from = 0

class Solver:
    # find the starting point, create new frontier
    def __init__(self, m):
        self.s = time.time()
        self.maze = m
        self.init = Node(self.find_block(start), None, None)
        self.frontier.add(self.init)
        self.count = 0
        self.solution = [x[:] for x in self.maze]
        self.explored = []
        self.solve()

    def solve(self):
        while True:
            # remove node from the frontier
            node = self.frontier.remove()
            state = node.state
            # if the state is goal state
            if self.maze[state[0]][state[1]] == end:
                self.e = time.time()
                self.time = self.e - self.s
                self.print_solution(node)
                break
            else:
                self.count += 1
                self.explored.append(node)
                neighbors = self.find_neighbors(node)
                # add neighboring blocks to the frontier, with current node as parent
                self.add_children(neighbors, node)

    def is_explored(self, state):
        return any(node.state == state for node in self.explored)

    #   1
    # 3 x 2
    #   0
    def find_neighbors(self, node):
        y,x = node.state
        n = []
        for direction,state in enumerate([(y+1, x), (y-1, x), (y, x+1), (y, x-1)]):
            n.append((state[0],state[1],direction))
        random.shuffle(n)
        return n

    def add_children(self, neighbors, node):
        for n in neighbors:
            i,j,d = n[0], n[1], n[2]
            if not self.is_explored((i,j)) and not self.frontier.contains_state((i,j)):
                if not self.maze[i][j] == wall:
                    child = Node((i,j), node, d)
                    self.frontier.add(child)

    def find_block(self, block):
        for row in self.maze:
            if block in row:
                return (self.maze.index(row), row.index(block))

    def print_solution(self, end_node):
        path = []
        node = end_node.parent
        while node.parent is not None:
            path.append(node.state)
            node = node.parent

        for c in path:
            y,x = c
            self.solution[y][x] = '*'

# ---------------------------------------- Algorithms -------------------------------------------------

'''
Searches every path to the end
'''
class Depth_first(Solver):
    def __init__(self, m):
        self.frontier = StackFrontier()
        super().__init__(m)

'''
Searches all paths at once
'''
class Breadth_first(Solver):
    def __init__(self, m):
        self.frontier = QueueFrontier()
        super().__init__(m)
'''
Picks the best node based on distance from the end
'''
class Best_first(Solver):
    def __init__(self, m, e = end):
        self.frontier = StackFrontier()
        self.maze = m
        self.height = len(self.maze)
        self.width = len(self.maze[0])
        self.end = self.find_block(e)
        super().__init__(m)

    def find_neighbors(self, node):
        y,x = node.state
        n = []
        calculated = []
        for direction,state in enumerate([(y+1, x), (y-1, x), (y, x+1), (y, x-1)]):
            m = self.manhattan_from(state, self.end)
            if m in calculated:
                if abs(abs(y - self.end[0]) - abs(x - self.end[1])) > (self.height+self.width)*0.04:
                    m += 0.5
                else:
                    m -= 0.5
            calculated.append(m)
            n.append((state[0],state[1],direction,m))
        # sort n based on distance from finish
        n.sort(key = lambda x:x[3])
        n.reverse()

        return n

    # manhattan distance from end_node
    def manhattan_from(self, state, from_state):
        return abs(from_state[0]-state[0]) + abs(from_state[1]-state[1])



def build(alg):
    solutions = []
    if 'D' in alg:
        x = Depth_first(maze)
        solutions.append((x.solution, x.count, 'depth', x.time))
    if 'B' in alg:
        x = Breadth_first(maze)
        solutions.append((x.solution, x.count, 'breadth', x.time))
    if 'G' in alg or solutions == []:
        x = Best_first(maze)
        solutions.append((x.solution, x.count, 'greedy best', x.time))
    return solutions

if __name__ == '__main__':
    solved = []
    try:
        width, height = int(sys.argv[1]), int(sys.argv[2])
        maze = creator.Maze(width, height).maze
        solved = build(sys.argv[3].upper())
        print_maze(maze)
        input()

    except:
        width, height = int(input('Width in characters: ')), int(input('Height in characters: '))
        maze = creator.Maze(width, height).maze
        print_maze(maze)
        print('Aglorithms (D - Depth first; B - Breadth first; G - Greedy best search)')
        algorithms = input('Pick one or more: ').upper()
        solved = build(algorithms)

    for s in solved:
        print_maze(s[0])
        print('count = ', s[1], f'({s[2]})', f'time={s[3]}')
