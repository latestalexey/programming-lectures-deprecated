# coding=utf-8
from tkinter import *
from itertools import chain
from collections import deque
from random import shuffle, randrange


class Maze(Frame):
    def __init__(self, width=600, height=600, vertical_cells=51,
                 horizontal_cells=51, border_width=0, keep_ratio=True,
                 field=None, colors=None, **kw):
        """
        Creates new TK app to display a maze

        :param width: maze width in px
        :param height: maze height in px
        :param vertical_cells: amount of vertical cells in maze
        :param horizontal_cells: amount of horizontal cells in maze
        :param border_width: border width
        :param keep_ratio: if `True`, adjust height to keep tiles square
        :param field: a maze of a walls. `field[x][y] == 1` means
                      `x`th `y`th tile is a wall (fills black).
                      If not provided a random maze will be generated.
                      Note that `vertical_cells` and `horizontal_cells`
                      will be raised to be odd.
                      In the random generated maze the enter is in (0, 0).
        :param colors: an array of colors mapped to tiles statuses.
                       `colors[0]` is for empty tile;
                       `colors[1]` is for wall;
                       Use others as you wish!

        """
        super().__init__(**kw)

        assert (width > 0 and
                height > 0 and
                vertical_cells > 0 and
                horizontal_cells > 0)

        if not colors:
            colors = ["white", "black", "red", "green", "blue"]

        self.colors = colors

        if field is None:
            vertical_cells += not (vertical_cells % 2)
            horizontal_cells += not (horizontal_cells % 2)
            self.field = list(self.make_maze(vertical_cells // 2,
                                             horizontal_cells // 2))

        self.width = width
        self.height = height

        if keep_ratio:
            self.height = self.width * vertical_cells / horizontal_cells

        self.vertical_cells = vertical_cells
        self.horizontal_cells = horizontal_cells
        self.vertical_size = self.height / vertical_cells
        self.horizontal_size = self.width / horizontal_cells

        self.pack()

        self.w = Canvas(self, width=self.width, height=self.height)
        self.w.pack()

        vs = self.vertical_size
        hs = self.horizontal_size

        for i in range(self.horizontal_cells):
            for j in range(self.vertical_cells):
                self.w.create_rectangle(i * hs, j * vs,
                                        (i + 1) * hs, (j + 1) * vs,
                                        fill=self.colors[self.field[i][j]],
                                        tags=('%s %s' % (i, j),),
                                        width=border_width)

    def fill_cell(self, i, j, color='white'):
        """
        Sets color of `(i, j)` tile to `color`

        :param i: vertical position
        :param j: horizontal position
        :param color: Tk color string

        """
        self.w.itemconfig('%s %s' % (i, j), fill=color)

    def fill_cell_from_color_index(self, i, j, color):
        if color > 2:
            color -= 2
            color %= len(self.colors) - 2
            color += 2
        self.fill_cell(i, j, self.colors[color])

    def clear_cell(self, i, j):
        """
        Sets color of `(i, j)` tile to white

        :param i: vertical position
        :param j: horizontal position

        """
        self.fill_cell(i, j)

    def status(self, i, j, status=None):
        """
        Sets status of `(i, j)` tile to `status`
        and changes its color according to `colors` array
        if `status` is specified. Returns current
        status of cell if not.

        :param i: vertical position
        :param j: horizontal position
        :param status: a new status of a tile

        """
        if status is None:
            return self.field[i][j]
        else:
            self.field[i][j] = status
            color = status
            if color > 2:
                color -= 2
                color %= len(self.colors) - 2
                color += 2

            self.fill_cell(i, j, self.colors[color])

    def neighbours(self, i, j):
        """
        Returns all neighbours of `(i, j)` tile

        :param i: vertical position
        :param j: horizontal position
        :return: tuple of coordinates
                 ((i - 1, j), (i, j - 1), (i + 1, j), (i, j + 1))

        """
        return ((i + x, j + y)
                for x, y in ((0, 1), (0, -1), (1, 0), (-1, 0))
                if (0 <= i + x < self.vertical_cells and
                    0 <= j + y < self.horizontal_cells))

    def call_async(self, f):
        """
        The decorator to allow delays without blocking I/O.

        Use `yield t` in a decorated function to sleep for `t`ms.

        """

        def handle_function(*args, **kwargs):
            gen = f(*args, **kwargs)

            def gen_run():
                try:
                    sleep = next(gen)
                except StopIteration:
                    return
                self.after(sleep, gen_run)

            gen_run()

        return handle_function

    @staticmethod
    def make_maze(w, h):
        # Private
        """
        Generates random maze with size `(2 * w, 2 * h)`.

        """
        vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
        ver = [[[1, 0]] * w + [[1]] for _ in range(h)] + [[]]
        hor = [[[1, 1]] * w + [[1]] for _ in range(h + 1)]

        def walk(x, y):
            q = deque()

            def walk_iter(x, y):

                vis[y][x] = 1

                d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
                shuffle(d)
                for (xx, yy) in d:
                    if vis[yy][xx]:
                        continue
                    if xx == x:
                        hor[max(y, yy)][x] = [1, 0]
                    if yy == y:
                        ver[y][max(x, xx)] = [0, 0]
                    yield (xx, yy)

            q.append(walk_iter(x, y))

            while len(q) > 0:
                try:
                    nx, ny = next(q[-1])
                    q.append(walk_iter(nx, ny))
                except StopIteration:
                    q.pop()

        walk(randrange(w), randrange(h))
        return chain.from_iterable(
            zip(map(lambda x: list(chain.from_iterable(x)), hor),
                map(lambda x: list(chain.from_iterable(x)), ver)))


if __name__ == "__main__":
    root = Tk()
    maze = Maze(master=root, vertical_cells=51, horizontal_cells=51)

    @maze.call_async
    def bfs():
        queue = []
        wave = 0

        while 1:
            s = len(queue)
            while s > 0:
                s -= 1
                for x, y in maze.neighbours(*queue.pop(0)):
                    if maze.status(x, y) != wave + 2 and maze.status(x, y) != 1:
                        queue.append((x, y))
                        maze.status(x, y, wave + 2)

            if not len(queue):
                wave += 1
                queue.append([1, 1])

            yield 1

    bfs()
    maze.mainloop()
