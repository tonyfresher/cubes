import random
from enum import Enum
from collections import defaultdict


class GameState:
    def __init__(self, field_size, colors_number):
        self.field_size = field_size
        self.colors = colors_number
        self._field = [[random.choice(list(CubeColor)[:self.colors])
                        for _ in range(self.field_size)]
                       for _ in range(self.field_size)]
        self._score = 0

    def exterminate(self, x, y):
        same = self.find_same_color(x, y)
        for cube_x, cube_y in same:
            self._field[cube_x][cube_y] = None
        for column in set([column for column, _ in same]):
            self.fall_column(column)
        for _ in range(self.field_size):
            self.fall_rows()

        self._score += self.block_value(len(same))
        self._cubes_left = self.count_cubes()

    def find_same_color(self, x, y):
        same = []
        self._find_same_color(x, y, same, self._field[x][y])
        return same

    def _find_same_color(self, x, y, block, color):
        if self.get_color(x, y) != color or (x, y) in block:
            return
        block.append((x, y))
        self._find_same_color(x - 1, y, block, color)
        self._find_same_color(x + 1, y, block, color)
        self._find_same_color(x, y - 1, block, color)
        self._find_same_color(x, y + 1, block, color)

    def fall_column(self, x):
        cubes = []
        for cube in self._field[x]:
            if cube:
                cubes.append(cube)
        new = []
        for _ in range(0, len(self._field[x]) - len(cubes)):
            new.append(None)
        for cube in cubes:
            new.append(cube)

        self._field[x] = new

    def fall_rows(self):
        for i in range(self.field_size):
            for cube in self._field[i]:
                if cube:
                    break
            else:
                del self._field[i]
                self._field.append([None for _ in range(self.field_size)])

    def count_block_value(self, x, y):
        if not self.get_color(x, y):
            return 0
        return self.block_value(len(self.find_same_color(x, y)))

    @staticmethod
    def block_value(count):
        return 2 ** (count - 1) - 1

    def count_cubes(self):
        cubes = defaultdict(lambda: 0)
        for x in range(self.field_size):
            for y in range(self.field_size):
                cubes[self.get_color(x, y)] += 1

        return dict(cubes)

    def get_color(self, x, y):
        if not (0 <= x < self.field_size and 0 <= y < self.field_size):
            return -1
        return self._field[x][y]

    def is_game_over(self):
        for x in range(self.field_size):
            for y in range(self.field_size):
                if self._field[x][y] and self.count_block_value(x, y) > 0:
                    return False
        return True

    @property
    def field(self):
        return self._field

    @property
    def score(self):
        return self._score


class CubeColor(Enum):
    RED = 1
    YELLOW = 2
    LIME = 3
    BLUE = 4
    ORANGE = 5
    VIOLET = 6
