from tkinter import Tk, Canvas


class Cell():
    FILLED_COLOR_BG = "green"
    EMPTY_COLOR_BG = "white"
    FILLED_COLOR_BORDER = "green"
    EMPTY_COLOR_BORDER = "white"

    def __init__(self, master, x, y, size, filled):
        """ Constructor of the object called by Cell(...) """
        self.master = master
        self.abs = x
        self.ord = y
        self.size = size
        self.filled = filled

    def switch(self):
        """ Switch if the cell is filled or not. """
        self.filled = not self.filled

    def fill(self):
        self.filled = 1

    def remove(self):
        self.filled = 0

    def draw(self):
        """ order to the cell to draw its representation on the canvas """
        if self.master is not None:
            filled = Cell.FILLED_COLOR_BG
            outline = Cell.FILLED_COLOR_BORDER

            if not self.filled:
                filled = Cell.EMPTY_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER

            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(
                xmin, ymin, xmax, ymax, fill=filled, outline=outline)


class CellGrid(Canvas):
    def __init__(self, master, rowNumber, columnNumber, cellSize, *args):
        Canvas.__init__(self, master, width=cellSize * columnNumber,
                        height=cellSize * rowNumber)

        self.cellSize = cellSize
        self.rowNumber = rowNumber
        self.columnNumber = columnNumber

        if not args:
            self.grid = []
            for row in range(rowNumber):

                line = []
                for column in range(columnNumber):
                    line.append(Cell(self, column, row, cellSize, 0))

                self.grid.append(line)
        else:
            self.grid = []
            for r, row in enumerate(args[0]):
                line = []
                for c, column in enumerate(row):
                    line.append(Cell(self, c, r, cellSize, column))
                self.grid.append(line)

        self.make_walls()

        # memorize the cells that have been modified
        self.switched = []

        # bind click action
        self.bind("<Button-1>", self.handleLeft)
        # bind click action
        self.bind("<Button-3>", self.handleRight)
        # bind moving while clicking
        self.bind("<B1-Motion>", self.handleLeftMotion)
        # bind moving while clicking
        self.bind("<B3-Motion>", self.handleRightMotion)
        # bind release button action - clear the memory of midified cells.
        self.bind("<ButtonRelease-1>", lambda event: self.switched.clear())

        self.draw()

    def make_walls(self):
        for x in range(self.rowNumber):
            for index, y in enumerate(self.grid[x]):
                if x == 0 or x == self.rowNumber - 1:
                    y.fill()
                else:
                    if index == 0 or index == self.columnNumber - 1:
                        y.fill()

    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()

    def _eventCoords(self, event):
        row = int(event.y / self.cellSize)
        column = int(event.x / self.cellSize)
        return row, column

    def handleLeft(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]
        cell.fill()
        cell.draw()
        # add the cell to the list of cell switched during the click
        self.switched.append(cell)

    def handleRight(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]
        cell.remove()
        cell.draw()
        # add the cell to the list of cell switched during the click
        self.switched.append(cell)

    def handleLeftMotion(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]

        if cell not in self.switched:
            cell.fill()
            cell.draw()
            self.switched.append(cell)

    def handleRightMotion(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]

        if cell not in self.switched:
            cell.remove()
            cell.draw()
            self.switched.append(cell)


if __name__ == "__main__":
    app = Tk()

    grid = CellGrid(app, 100, 180, 10)
    grid.pack()

    app.mainloop()
