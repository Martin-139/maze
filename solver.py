import creator, random
maze = creator.Maze(50, 50).maze

def print_maze(maze):
    for r in maze:
        print(''.join(x for x in r))
    print('-' * 25)

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
    global maze
    frontier = StackFrontier()
    explored = []

    # find the starting point, create new frontier
    def __init__(self):
        self.init = Node(self.find_block('A '), None, None)
        self.frontier.add(self.init)
        self.count = 0
        self.solve()

    def solve(self):
        while True:
            # remove node from the frontier
            node = self.frontier.remove()
            state = node.state
            # if the state is goal state
            if maze[state[0]][state[1]] == ' B':
                print('Count:', self.count)
                self.print_solution(node)
                break
            else:
                self.count += 1
                self.explored.append(node)
                neighbors = self.find_neighbors(node)
                # add neighboring blocks to the frontier, with current node as parent
                random.shuffle(neighbors)
                for n in neighbors:
                    i,j,d = n
                    if not self.is_explored((i,j)) and not self.frontier.contains_state((i,j)):
                        if not maze[i][j] == '[]':
                            child = Node((i,j), node, d)
                            self.frontier.add(child)


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
        return n


    def find_block(self, block):
        for row in maze:
            if block in row:
                return (maze.index(row), row.index(block))

    def print_solution(self, end_node):
        path = []
        node = end_node.parent
        while node.parent is not None:
            path.append(node.state)
            node = node.parent

        for c in path:
            y,x = c
            maze[y][x] = '**'




if __name__ == '__main__':
    print_maze(maze)
    s = Solver()
    x = input()
    print_maze(maze)
