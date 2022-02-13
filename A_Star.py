import creator, solver
import time

start = 3
end = 4
wall = 1
cell = 2

class Node:
    def __init__(self, state, tentative_dist=float('inf')):
        self.state = state
        self.tentative_dist = tentative_dist
        self.neighbors = []
        self.parent = None
        self.manhattan = 0
        self.heuristic = self.tentative_dist + self.manhattan

    def update_heuristic(self):
        self.heuristic = self.tentative_dist + self.manhattan

    def add_neighbor(self, node, dist):
        self.neighbors.append((node, dist))

class Frontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def sort(self):
        self.frontier.sort(key = lambda x:x.heuristic)

'''
Create 'nodes' on intersections instead of looking on every block.
Then find the shortest path based on distance between neighboring nodes.
'''
class Dijkstra():
    def __init__(self, m):
        self.maze = [x[:] for x in m]
        self.height = len(self.maze)
        self.width = len(self.maze[0])
        self.frontier = Frontier()
        self.solution = [x[:] for x in self.maze]
        self.end = self.find_block(end)
        self.create_nodes()
        # self.all_paths() # experimental
        self.solve()

    def create_nodes(self):
        # checks every block and finds nodes (intersections)
        for y, row in enumerate(self.maze):
            for x, block in enumerate(row):
                node = None
                if block == cell:
                    n = self.get_neighbors(y,x)
                    # 2 neighbors
                    if len(n) == 2:
                        if not abs(n[0][0] - n[1][0]) == 1:
                            continue
                    # 1 neighbor
                    elif len(n) == 1:
                        continue
                    node = Node(state=(y,x))

                elif block == start:
                    node = Node(state=(y,x), tentative_dist=0)
                elif block == end:
                    node = Node(state=(y,x))

                # count distance from nearest neighbor and add it to list
                if node:
                    self.maze[y][x] = node
                    self.frontier.add(node)
                    for direction in range(2):
                        i,j = y,x
                        dist = 0
                        while True:
                            if direction == 1:
                                i -= 1
                            else:
                                j -= 1
                            dist += 1
                            current = self.maze[i][j]
                            if current == wall:
                                break
                            if isinstance(current, Node):
                                current.add_neighbor(node, dist)
                                node.add_neighbor(current, dist)
                                break
                    if node.manhattan == 0:
                        node.manhattan = self.manhattan(node)
        self.frontier.sort()

    def get_neighbors(self, y, x):
        n = []
        for state in [(y+1, x), (y-1, x), (y, x+1), (y, x-1)]:
            i,j = state
            try:
                if not self.maze[i][j] == wall:
                    n.append((i,j))
            except:
                pass
        return n

    def print_nodes(self):
        for n in self.frontier.frontier:
            self.maze[n.state[0]][n.state[1]] = '*'
        # solver.print_maze(self.maze)
    # remove all paths, that don't lead anywhere (only 1 neighbor)
    def all_paths(self):
        while True:
            new_state = self.frontier.frontier.copy()
            for n in new_state:
                if len(n.neighbors) == 1 and not n.state == self.end:
                    new_state.remove(n)
                    neighbor, dist = n.neighbors[0][0], n.neighbors[0][1]
                    neighbor.neighbors.remove((n, dist))
            if self.frontier.frontier == new_state:
                break
            else:
                self.frontier.frontier = new_state.copy()
        self.print_nodes()

    def solve(self):
        self.visited = []
        self.unvisited = Frontier()
        self.unvisited.add(self.frontier.frontier[0])
        fin = False
        self.count = 0
        while True:
            # next node is the first in unvisited
            node = self.unvisited.frontier[0]
            for neighbor in node.neighbors:
                n_node, distance = neighbor
                if n_node not in self.visited:

                    # if we hit the goal
                    if n_node.state == self.end:
                        n_node.parent = node
                        self.end_node = n_node
                        fin = True
                        break

                    # count the tentative distance
                    old = n_node.tentative_dist
                    new = distance + node.tentative_dist
                    if old is not float('inf'):
                        if new < old:
                            n_node.tentative_dist = new
                            n_node.parent = node
                    else:
                        n_node.tentative_dist = new
                        n_node.parent = node
                    n_node.update_heuristic()

                    self.unvisited.add(n_node)


            self.visited.append(node)
            self.count += 1
            self.unvisited.sort()
            self.unvisited.frontier.pop(0)
            if fin:
                break
        self.frontier.sort()
        # print('\n'.join(str(x.state)+','+str(x.heuristic) for x in self.frontier.frontier))
        self.print_solution()

    def manhattan(self, node):
        return 1

    def print_solution(self):
        path = []
        node = self.end_node
        while node.parent is not None:
            path.append(node.state)
            node = node.parent
        path.append(node.state)

        path = self.fill_path(path)

        for c in path:
            y,x = c
            self.solution[y][x] = '*'
            i,j = self.end_node.state
            self.solution[i][j] = end
            i,j = node.state
            self.solution[i][j] = end

        solver.print_maze(self.solution)

    def fill_path(self, path):
        new_path = []
        for index, state in enumerate(path):
            y,x = state
            try:
                y2, x2 = path[index + 1]
                # on the same X
                if y2 == y:
                    if x2 < x:
                        while not x2 == x+1:
                            new_path.append((y, x2))
                            x2 += 1
                    else:
                        while not x2+1 == x:
                            new_path.append((y, x))
                            x += 1
                else:
                    if y2 < y:
                        while not y2 == y+1:
                            new_path.append((y2, x))
                            y2 += 1
                    else:
                        while not y2+1 == y:
                            new_path.append((y, x))
                            y += 1
            except:
                pass
        return new_path

    def find_block(self, block):
        for row in self.maze:
            if block in row:
                return (self.maze.index(row), row.index(block))

class A_star(Dijkstra):
    def __init__(self, m):
        super().__init__(m)

    def manhattan(self, node):
        state = node.state
        return abs(self.end[0]-state[0]) + abs(self.end[1]-state[1])


if __name__ == '__main__':
    m = creator.Maze(100,50).maze
    s = time.time()

    d = A_star(m)
    # d = Dijkstra(m)

    e = time.time()
    print(e-s, d.count)
