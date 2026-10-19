
import unittest

from task1_python_debugging import unique_values

class TestUniqueValues(unittest.TestCase):

    def test_removes_duplicates(self):
        self.assertEqual(unique_values([1, 2, 2, 3]), [1, 2, 3])

    def test_empty_input(self):
        self.assertEqual(unique_values([]), [])

    def test_preserves_original_order(self):
        self.assertEqual(
            unique_values([3, 1, 2, 1, 3]),
            [3, 1, 2],
        )

    def test_does_not_modify_input(self):
        values = [1, 2, 2, 3]
        original = values.copy()

        unique_values(values)

        self.assertEqual(values, original)

    def test_supports_unhashable_elements(self):
        self.assertEqual(
            unique_values([[1], [2], [1]]),
            [[1], [2]],
        )

    def test_accepts_generator(self):
        values = (x for x in [1, 1, 2, 3, 2])
        self.assertEqual(unique_values(values), [1, 2, 3])


if __name__ == "__main__":
    unittest.main(verbosity=2)