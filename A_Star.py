import creator, solver
import time

class Node:
    def __init__(self, state, tentative_dist=float('inf')):
        self.state = state
        self.tentative_dist = tentative_dist
        self.neighbors = []

    def add_neighbor(self, node, dist):
        self.neighbors.append((node, dist))

class Frontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)
        self.frontier.sort(key = lambda x:x.tentative_dist)

class Dijkstra():
    def __init__(self, m):
        self.maze = m
        self.frontier = Frontier()
        self.create_nodes()
        self.print_nodes()

    def create_nodes(self):
        for y, row in enumerate(self.maze):
            for x, block in enumerate(row):
                if block == 2:
                    n = self.get_neighbors(y,x)
                    if len(n) == 2:
                        if not abs(n[0][0] - n[1][0]) == 1:
                            continue
                    elif len(n) == 1:
                        continue
                    node = Node(state=(y,x))
                    self.frontier.add(node)
                    self.maze[y][x] = node

                    i,j = y-1,x
                    dist = 0
                    while True:
                        dist += 1
                        current = self.maze[i][j]
                        if current == 1:
                            break
                        if isinstance(current, Node):
                            current.add_neighbor(node, dist)
                            node.add_neighbor(node, dist)
                            break
                        i -= 1
                    i,j = y,x-1
                    dist = 0
                    while True:
                        dist += 1
                        current = self.maze[i][j]
                        if current == 1:
                            break
                        if isinstance(current, Node):
                            current.add_neighbor(node, dist)
                            node.add_neighbor(node, dist)
                            break
                        j -= 1
                elif block == 3:
                    self.frontier.add(Node(state=(y,x), tentative_dist=0))
                elif block == 4:
                    self.frontier.add(Node(state=(y,x)))
                    self.end = (y,x)

    def get_neighbors(self, y, x):
        n = []
        for state in [(y+1, x), (y-1, x), (y, x+1), (y, x-1)]:
            i,j = state
            try:
                if not self.maze[i][j] == 1:
                    n.append((i,j))
            except:
                pass
        return n

    def print_nodes(self):
        for n in self.frontier.frontier:
            self.maze[n.state[0]][n.state[1]] = '*'
            # print(' '.join(str(x[0].state) + '-' + str(x[1]) for x in n.neighbors))
        solver.print_maze(self.maze)

if __name__ == '__main__':
    s = time.time()
    m = creator.Maze(100,50).maze
    t = time.time()
    d = Dijkstra(m)
    e = time.time()
    print(t-s, e-t)
