# coding=utf-8
from tkinter import *
from itertools import chain
from collections import deque
from random import shuffle, randrange


class Maze(Frame):
    def __init__(self, width=600, height=600, vertical_cells=51,
                 horizontal_cells=51, border_width=0,
                 keep_ratio=True, field=None, **kw):
        """
        Creates new TK app to display a maze

        :param border_width: border width
        :param width: maze width in px
        :param height: maze height in px
        :param vertical_cells: amount of vertical cells in maze
        :param horizontal_cells: amount of horizontal cells in maze
        :param keep_ratio: if `True`, adjust height to keep tiles square
        :param field: a maze of a walls. `field[x][y] == 1` means
                      `x`th `y`th tile is a wall (fills black).
                      If not provided a random maze will be generated.
                      Note that `vertical_cells` and `horizontal_cells`
                      will be raised to be odd.
                      In the random generated maze the enter is in (0, 0).
        """
        super().__init__(**kw)

        assert (width > 0 and
                height > 0 and
                vertical_cells > 0 and
                horizontal_cells > 0)

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
                                        fill=('black'
                                              if self.field[i][j] else
                                              'white'),
                                        tags=('%s %s' % (i, j),),
                                        width=border_width)

    def fill_cell(self, i, j, color='white'):
        self.w.itemconfig('%s %s' % (i, j), fill=color)

    def clear_cell(self, i, j):
        self.fill_cell(i, j)

    def call_async(self, f):
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

    colors = ["red", "green", "blue", "white"]

    @maze.call_async
    def bfs():
        queue = []
        positions = ((0, 1), (0, -1), (1, 0), (-1, 0))
        step = 1
        wave = 4

        while 1:
            s = len(queue)
            step += 1
            while s > 0:
                s -= 1
                xi, xj = queue.pop(0)
                for i, j in positions:
                    x, y = xi + i, xj + j
                    if 0 <= x < 51 and 0 <= y < 51:
                        if maze.field[x][y] != wave and maze.field[x][y] != 1:
                            queue.append((x, y))
                            maze.field[x][y] = wave
                            maze.fill_cell(x, y, colors[wave % len(colors)])

            if not len(queue):
                wave += 1
                queue.append([1, 1])

            yield 1

    bfs()
    maze.mainloop()
