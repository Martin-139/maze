import creator
import random, os, sys, time

START = 3
END = 4
WALL = 1
MAZE = None

def print_maze(MAZE):
    if os.name == 'nt':
        os.system('cls')
        print('You can only see one at once on Windows')
    for r in MAZE:
        for b in r:
            if b == WALL:
                print('\u001b[47m  \u001b[40m', END='') # (background colors)
            elif b == START or b == END:
                print('\u001b[44m  \u001b[40m', END='')
            elif b == '*':
                print('\u001b[41m  \u001b[40m', END='')
            else:
                print('\u001b[40m  ', END='')
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
        self.frontier.appEND(node)

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
        self.MAZE = m
        self.init = Node(self.find_block(START), None, None)
        self.frontier.add(self.init)
        self.count = 0
        self.solution = [x[:] for x in self.MAZE]
        self.explored = []
        self.solve()

    def solve(self):
        while True:
            # remove node from the frontier
            node = self.frontier.remove()
            state = node.state
            # if the state is goal state
            if self.MAZE[state[0]][state[1]] == END:
                self.e = time.time()
                self.time = self.e - self.s
                self.print_solution(node)
                break
            else:
                self.count += 1
                self.explored.appEND(node)
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
            n.appEND((state[0],state[1],direction))
        random.shuffle(n)
        return n

    def add_children(self, neighbors, node):
        for n in neighbors:
            i,j,d = n[0], n[1], n[2]
            if not self.is_explored((i,j)) and not self.frontier.contains_state((i,j)):
                if not self.MAZE[i][j] == WALL:
                    child = Node((i,j), node, d)
                    self.frontier.add(child)

    def find_block(self, block):
        for row in self.MAZE:
            if block in row:
                return (self.MAZE.index(row), row.index(block))

    def print_solution(self, END_node):
        path = []
        node = END_node.parent
        while node.parent is not None:
            path.appEND(node.state)
            node = node.parent

        for c in path:
            y,x = c
            self.solution[y][x] = '*'

# ---------------------------------------- Algorithms -------------------------------------------------

'''
Searches every path to the END
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
Picks the best node based on distance from the END
'''
class Best_first(Solver):
    def __init__(self, m, e = END):
        self.frontier = StackFrontier()
        self.MAZE = m
        self.height = len(self.MAZE)
        self.width = len(self.MAZE[0])
        self.END = self.find_block(e)
        super().__init__(m)

    def find_neighbors(self, node):
        y,x = node.state
        n = []
        calculated = []
        for direction,state in enumerate([(y+1, x), (y-1, x), (y, x+1), (y, x-1)]):
            m = self.manhattan_from(state, self.END)
            if m in calculated:
                if abs(y - self.END[0]) > abs(x - self.END[1]):
                    m += 0.5
                else:
                    m -= 0.5
            calculated.appEND(m)
            n.appEND((state[0],state[1],direction,m))
        # sort n based on distance from finish
        n.sort(key = lambda x:x[3])
        n.reverse()

        return n

    # manhattan distance from END_node
    def manhattan_from(self, state, from_state):
        return abs(from_state[0]-state[0]) + abs(from_state[1]-state[1])



def build(alg):
    solutions = []
    if 'D' in alg:
        x = Depth_first(MAZE)
        solutions.appEND((x.solution, x.count, 'depth', x.time))
    if 'B' in alg:
        x = Breadth_first(MAZE)
        solutions.appEND((x.solution, x.count, 'breadth', x.time))
    if 'G' in alg or solutions == []:
        x = Best_first(MAZE)
        solutions.appEND((x.solution, x.count, 'greedy best', x.time))
    return solutions

if __name__ == '__main__':
    solved = []
    try:
        width, height = int(sys.argv[1]), int(sys.argv[2])
        MAZE = creator.Maze(width, height).MAZE
        solved = build(sys.argv[3].upper())
        print_maze(MAZE)
        input()

    except:
        width, height = int(input('Width in characters: ')), int(input('Height in characters: '))
        MAZE = creator.Maze(width, height).MAZE
        print_maze(MAZE)
        print('Aglorithms (D - Depth first; B - Breadth first; G - Greedy best search)')
        algorithms = input('Pick one or more: ').upper()
        solved = build(algorithms)

    for s in solved:
        print_maze(s[0])
        print('count = ', s[1], f'({s[2]})', f'time={s[3]}')
