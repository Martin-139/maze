import creator, solver

class Node:
    def __init__(self, state, tentative_dist=float('inf')):
        self.state = state
        self.tentative_dist = tentative_dist
        self.neighbors = []

    def add_neighbor(self, node):
        self.neighbors.append(node)

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
                if block == 'A':
                    self.frontier.add(Node(state=(y,x), tentative_dist=0))
                elif block == '  ':
                    n = self.get_neighbors(y,x)
                    if len(n) == 2:
                        if not abs(n[0][0] - n[1][0]) == 1:
                            continue
                    node = Node(state=(y,x))
                    self.frontier.add(node)
                    i,j = y-1,x
                    while True:
                        if self.maze[i][j] == '[]':
                            break
                        if any(node.state == (i,j) for node in self.frontier.frontier):
                            for up in self.frontier.frontier:
                                if up.state == (i,j):
                                    up.add_neighbor(node)
                                    node.add_neighbor(up)
                                    break
                            break
                        i -= 1
                    i,j = y,x-1
                    while True:
                        if self.maze[i][j] == '[]':
                            break
                        if any(node.state == (i,j) for node in self.frontier.frontier):
                            for up in self.frontier.frontier:
                                if up.state == (i,j):
                                    up.add_neighbor(node)
                                    node.add_neighbor(up)
                                    break
                        j -= 1


    def get_neighbors(self, y, x):
        n = []
        for state in [(y+1, x), (y-1, x), (y, x+1), (y, x-1)]:
            i,j = state
            try:
                if self.maze[i][j] == '  ' or self.maze[i][j] == 'B':
                    n.append((state[0],state[1]))
            except:
                pass
        return n

    def print_nodes(self):
        for n in self.frontier.frontier:
            self.maze[n.state[0]][n.state[1]] = '*'
            print(' '.join(str(x.state) for x in n.neighbors))
        solver.print_maze(self.maze)

if __name__ == '__main__':
    d = Dijkstra(creator.Maze(100,50).maze)
