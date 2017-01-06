import unittest
from model import GameState


class Test(unittest.TestCase):
    def setUp(self):
        self.gs = GameState(10, 1)

    def test_params(self):
        self.assertEqual(10, self.gs.field_size)
        colors = set()
        for row in self.gs.field:
            for cube in row:
                colors.add(cube)
        self.assertEqual(1, len(colors))

    def test_exterminate(self):
        self.gs.exterminate(0, 0)
        for row in self.gs.field:
            for cube in row:
                self.assertIsNone(cube)

    def test_fall_column(self):
        self.gs._field[0][9] = None
        self.gs._field[0][7] = None
        self.gs._field[0][5] = None
        self.gs.fall_column(0)
        self.assertIsNotNone(self.gs._field[0][9])
        self.assertIsNotNone(self.gs._field[0][7])
        self.assertIsNotNone(self.gs._field[0][5])

    def test_fall_rows(self):
        self.gs._field[1] = [None] * 10
        self.gs._field[3] = [None] * 10
        self.gs._field[5] = [None] * 10
        self.gs.fall_rows()
        with self.assertRaises(AssertionError):
            self.assertSequenceEqual([None] * 10, self.gs._field[1])
        with self.assertRaises(AssertionError):
            self.assertSequenceEqual([None] * 10, self.gs._field[3])
        with self.assertRaises(AssertionError):
            self.assertSequenceEqual([None] * 10, self.gs._field[5])

    def test_find_sames(self):
        self.assertEqual(10 * 10, len(self.gs.find_same_color(0, 0)))

    def test_counting_cubes(self):
        gs = GameState(10, 5)
        by_colors = gs.count_cubes()
        cubes = 0
        for color in by_colors:
            cubes += by_colors[color]

        self.assertEqual(10 * 10, cubes)

    def test_game_over(self):
        self.assertFalse(self.gs.is_game_over())
        self.gs.exterminate(0, 0)
        self.assertTrue(self.gs.is_game_over())

if __name__ == '__main__':
    unittest.main()
