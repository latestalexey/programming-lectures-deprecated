# coding=utf-8
import tkinter as tk
import collections
import itertools
import math
import random


class Maze(tk.Frame):
    def __init__(self, width=600, height=600, vertical_cells=51,
                 horizontal_cells=51, border_width=0, keep_ratio=True,
                 field=None, colors=None, sparseness=0.0, **kw):
        """
        Creates new TK app to display a maze

        :param width: maze width in px
        :param height: maze height in px
        :param vertical_cells: amount of vertical cells in maze
        :param horizontal_cells: amount of horizontal cells in maze
        :param border_width: border width
        :param keep_ratio: if `True`, adjust height and width
                           to keep tiles square
        :param field: a maze of a walls. `field[x][y] == 1` means
                      `x`th `y`th tile is a wall (fills black).
                      If not provided a random maze will be generated.
                      Note that `vertical_cells` and `horizontal_cells`
                      will be raised to be odd.
        :param colors: an array of colors which will be mapped to tile
                       statuses.
                       `colors[0]` is for empty tile;
                       `colors[1]` is for wall;
                       Use others as you wish!
        :param sparseness: used in maze generator if `field` is not set.
                           Set this to `0` to get a tree (only one path between
                           any two points) or to `2` to get a blank maze.

        """
        super().__init__(**kw)

        assert (width > 0 and
                height > 0 and
                vertical_cells > 0 and
                horizontal_cells > 0 and
                0 <= sparseness <= 2)

        if colors is None:
            colors = ["white", "black", "red", "green", "blue"]

        self.colors = colors

        if field is None:
            vertical_cells += not (vertical_cells % 2)
            horizontal_cells += not (horizontal_cells % 2)
            self.field = self._make_maze(vertical_cells // 2,
                                         horizontal_cells // 2,
                                         sparseness)

        self.width = width
        self.height = height

        if keep_ratio:
            new_height = self.width * vertical_cells / horizontal_cells
            if new_height > self.height:
                ratio = self.height / new_height
                new_height *= ratio
                self.width *= ratio
            self.height = new_height

        self.vertical_cells = vertical_cells
        self.horizontal_cells = horizontal_cells
        self.vertical_size = self.height / vertical_cells
        self.horizontal_size = self.width / horizontal_cells

        self.pack()

        self.w = tk.Canvas(self, width=self.width, height=self.height)
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

            self._fill_cell(i, j, self.colors[color])

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
                if (0 <= i + x < self.horizontal_cells and
                    0 <= j + y < self.vertical_cells))

    def call_async(self, f):
        """
        Decorator allows delays without blocking I/O.

        Use `yield t` in a decorated function to sleep for `t`ms.

        """

        def handle_function(*args, **kwargs):
            gen = f(*args, **kwargs)
            sleep = 0

            def gen_run():
                nonlocal sleep
                while sleep < 1:
                    try:
                        sleep += next(gen)
                    except StopIteration:
                        return
                sleep_now = math.floor(sleep)
                sleep -= sleep_now
                self.after(sleep_now, gen_run)

            gen_run()

        return handle_function

    def _fill_cell(self, i, j, color='white'):
        """
        Sets color of `(i, j)` tile to `color`

        :param i: vertical position
        :param j: horizontal position
        :param color: Tk color string

        """
        if isinstance(color, int):
            if color > 2:
                color -= 2
                color %= len(self.colors) - 2
                color += 2
            color = self.colors[color]
        self.w.itemconfig('%s %s' % (i, j), fill=color)

    def _clear_cell(self, i, j):
        # Private
        """
        Sets color of `(i, j)` tile to white

        :param i: vertical position
        :param j: horizontal position

        """
        self._fill_cell(i, j)

    @staticmethod
    def _make_maze(w, h, sparseness=0.0):
        # Private
        """
        Generates a random maze sized `(2 * w, 2 * h)`.

        """
        vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
        ver = [[[1, 0]] * w + [[1]] for _ in range(h)] + [[]]
        hor = [[[1, 1]] * w + [[1]] for _ in range(h + 1)]

        def walk(x, y):
            q = collections.deque()

            def walk_iter(x, y):
                vis[y][x] = 1
                d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
                random.shuffle(d)
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

        walk(random.randrange(w), random.randrange(h))
        result = list(itertools.chain.from_iterable(
            zip(map(lambda x: list(itertools.chain.from_iterable(x)), hor),
                map(lambda x: list(itertools.chain.from_iterable(x)), ver))))

        for i in range(1, len(result) - 2):
            for j in range(1, len(result[i]) - 1):
                if (result[i][j] and
                    ((result[i][j - 1] == 0 and
                      result[i][j + 1] == 0 and
                      result[i + 1][j] == 1 and
                      result[i - 1][j] == 1) or
                     (result[i][j - 1] == 1 and
                      result[i][j + 1] == 1 and
                      result[i + 1][j] == 0 and
                      result[i - 1][j] == 0)) and
                        0 < random.random() <= sparseness) or 0 < random.random() <= sparseness - 1:
                    result[i][j] = 0

        return result


if __name__ == "__main__":
    root = tk.Tk()
    maze = Maze(master=root,
                vertical_cells=20,
                horizontal_cells=20,
                sparseness=0.2)

    @maze.call_async
    def dfs():
        queue = collections.deque()
        wave = 0

        while 1:
            if not len(queue):
                wave += 1
                queue.append((1, 1))

            for x, y in maze.neighbours(*queue.pop()):
                if maze.status(x, y) != wave + 2 and maze.status(x, y) != 1:
                    queue.append((x, y))
                    maze.status(x, y, wave + 2)

            yield 0.5

    # dfs()

    maze.mainloop()
