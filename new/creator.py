import sys
import random
import os
import board
from tkinter import Tk

# Randomized Prim's algorithm
# with the way the maze is built, it is solvable when you go from anywhere to anywhere

WALL = 1
CELL = 0
START, END = 3, 4


class Maze:
    # initialize and create maze full of 'unvisited' blocks
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.wall = WALL
        self.cell = CELL
        self.edge = 5
        self.walls = []

        full = []
        for i in range(height):
            line = []
            for j in range(width):
                if i == 0 or j == 0 or i == self.height-1 or j == self.width-1:
                    line.append(self.edge)
                else:
                    line.append(self.wall)
            full.append(line)
        self.maze = full

        self.create()

    def create(self):
        # pick random wall to start
        start_x = random.randint(1, self.width-2)
        start_y = random.randint(1, self.height-2)
        self.maze[start_y][start_x] = self.cell
        self.setwalls(start_y, start_x)

        # while there are still walls in the list
        while self.walls:
            # pick random wall
            rand = random.choice(self.walls)
            # check if the wall has right neighbors
            new_cell = self.check_wall(rand)
            if not new_cell == False:
                try:
                    y, x = new_cell[0], new_cell[1]
                    self.maze[y][x] = self.cell
                    self.maze[rand[0]][rand[1]] = self.cell
                    self.setwalls(y, x)
                except IndexError:
                    pass  # just don't create a path (probably out of bounds)

            # remove wall from the list
            self.walls.remove(rand)

        # make remaining 'edges' a wall
        for row in range(len(self.maze)):
            self.maze[row][0] = self.wall
            self.maze[row][self.width-1] = self.wall
        for col in range(len(self.maze[0])):
            self.maze[0][col] = self.wall
            self.maze[self.height-1][col] = self.wall

        self.maze[self.height-2][1] = 3
        self.maze[1][self.width-2] = 4

    # add walls around a block to list
    def setwalls(self, y, x):
        for i, j in [(y+1, x), (y-1, x), (y, x+1), (y, x-1)]:
            try:
                if not self.maze[i][j] == self.cell and not self.maze[i][j] == self.edge:
                    # self.maze[i][j] = self.wall (no longer needed when 'unvisited' is not used - possible bug later?)
                    self.walls.append((i, j))
            except IndexError:
                pass

    # check if from the wall's neighboring blocks there is only one cell (+ return new cell's coordinates)
    def check_wall(self, wall):
        y, x = wall[0], wall[1]
        cells = 0
        location = None
        for i, j in [(y+1, x), (y-1, x), (y, x+1), (y, x-1)]:
            if self.maze[i][j] == self.cell:
                cells += 1
                location = (i, j)
        if cells == 1:
            # this formula finds the coordiantions of new cell (x or y raises/lowers by 2 appropriately)
            new_y = location[0] - 2*(location[0]-y)
            new_x = location[1] - 2*(location[1]-x)
            # this condition doesn't make any sense but is essential for the maze
            if self.maze[new_y][new_x] == self.wall:
                return (new_y, new_x) if new_y >= 0 and new_x >= 0 else False
            # prevent 'doubled edge' by changing the wall to cell if new_cell is supposed to be on the edge
            else:
                self.maze[y][x] = self.cell
                self.setwalls(y, x)
        return False


def print_maze(maze):
    if os.name == 'nt':
        os.system('cls')
        print('You can only see one at once on Windows')
    for r in maze:
        for b in r:
            if b == WALL:
                print('\u001b[47m  \u001b[40m', end='')  # (background colors)
            elif b == START or b == END:
                print('\u001b[44m  \u001b[40m', end='')
            elif b == '*':
                print('\u001b[41m  \u001b[40m', end='')
            else:
                print('\u001b[40m  ', end='')
        print()


if __name__ == '__main__':
    m = Maze(int(sys.argv[1]), int(sys.argv[2]))
    print_maze(m.maze)

    app = Tk()
    grid = board.CellGrid(app, int(sys.argv[2]),int(sys.argv[1]), 10, m.maze)
    grid.pack()
    app.mainloop()
