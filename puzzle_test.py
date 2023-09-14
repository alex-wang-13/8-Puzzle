import unittest
import io
import sys

# Import the required class.
from puzzle import Puzzle
from puzzle import Direction

class PuzzleTestCase(unittest.TestCase):

    def tearDown(self) -> None:
        """
        Resets the puzzle after each test case.
        """
        
        Puzzle.reset_puzzle()
        return super().tearDown()

    def test_action(self):
        Puzzle.action("setState 012 345 678")
        self.assertEqual(Puzzle.state, [i for i in range(9)])
        Puzzle.action("setState 876 543 210")
        self.assertEqual(Puzzle.state, [8, 7, 6, 5, 4, 3, 2, 1, 0])
        # Testing ValueErrors.
        # Erroneously accepts a length 9 state argument outside the range [0, 8].
        self.assertRaises(ValueError, Puzzle.action, command="setState 123 456 789")
        # Erroneously accepts a length 9 argument with duplicate numbers.
        self.assertRaises(ValueError, Puzzle.action, command="setState 011 345 688")
        # "Erroneously accepts a length 9 argument with one duplicate number.
        self.assertRaises(ValueError, Puzzle.action, command="setState 001 345 689")
        # Erroneously accepts a length 10 argument.
        self.assertRaises(ValueError, Puzzle.action, command="setState 012 345 6789")
        # Erroneously accepts a length 1 argument.
        self.assertRaises(ValueError, Puzzle.action, command="setState 0")
        # Erroneously accepts a length 0 argument.
        self.assertRaises(ValueError, Puzzle.action, command="setState")

    def test_init_state(self):
        self.assertEqual(Puzzle.state, [], msg="The puzzle state is not initially an empty list.")
        self.assertFalse(Puzzle.valid, msg="The puzzle is initially valid when it should be invalid.")

    def test_set_state(self):
        test_state1 = "012 345 678"
        Puzzle.set_state(state=test_state1)
        self.assertEqual(Puzzle.state, [i for i in range(9)])
        self.assertTrue(Puzzle.valid)

        Puzzle.reset_puzzle()
        self.assertEqual(Puzzle.state, [], msg="The puzzle state is not reset an empty list.")
        self.assertFalse(Puzzle.valid, msg="The puzzle is valid when it should be reset to invalid.")

        test_state2 = "547 683 210"
        Puzzle.set_state(state=test_state2)
        self.assertEqual(Puzzle.state, [int(c) for c in test_state2.replace(" ", "")])
        self.assertTrue(Puzzle.valid)

    def test_set_state_robust(self):
        # Tests a state that is formatted slightly incorrectly (should pass).
        test_state1 = "012345678"
        Puzzle.set_state(state=test_state1)
        self.assertEqual(Puzzle.state, [i for i in range(9)])
        self.assertTrue(Puzzle.valid)

    def test_set_state_exception(self):
        # Erroneously accepts a length 9 state argument outside the range [0, 8].
        self.assertRaises(ValueError, Puzzle.set_state, state="123456789")
        # Erroneously accepts a length 9 argument with duplicate numbers.
        self.assertRaises(ValueError, Puzzle.set_state, state="011345688")
        # "Erroneously accepts a length 9 argument with one duplicate number.
        self.assertRaises(ValueError, Puzzle.set_state, state="001345689")
        # Erroneously accepts a length 10 argument.
        self.assertRaises(ValueError, Puzzle.set_state, state="0123456789")
        # Erroneously accepts a length 1 argument.
        self.assertRaises(ValueError, Puzzle.set_state, state=" 0")
        # Erroneously accepts a length 0 argument.
        self.assertRaises(ValueError, Puzzle.set_state, state="")

    def test_print_state(self):
        output: io.StringIO = io.StringIO()
        sys.stdout = output
        # Empty/Invalid print_state.
        Puzzle.print_state()
        self.assertEqual(output.getvalue().strip(), "".strip())
        # Standard print_state.
        Puzzle.set_state("012345678")
        Puzzle.print_state()
        self.assertEqual(output.getvalue().strip(), "0 1 2\n3 4 5\n6 7 8\n".strip())
        # Standard print_state.
        output: io.StringIO = io.StringIO()
        sys.stdout = output
        Puzzle.set_state("876543210")
        Puzzle.print_state()
        self.assertEqual(output.getvalue().strip(), "8 7 6\n5 4 3\n2 1 0\n".strip())
        sys.stdout = sys.__stdout__

    def test_move(self):
        Puzzle.set_state("012345678")
        Puzzle.move(Direction.DOWN)
        self.assertEqual(Puzzle.state, [3, 1, 2, 0, 4, 5, 6, 7, 8], msg="Did not move the blank tile down.")
        Puzzle.move(Direction.RIGHT)
        self.assertEqual(Puzzle.state, [3, 1, 2, 4, 0, 5, 6, 7, 8], msg="Did not move the blank tile right.")
        Puzzle.move(Direction.RIGHT)
        self.assertEqual(Puzzle.state, [3, 1, 2, 4, 5, 0, 6, 7, 8], msg="Did not move the blank tile right.")
        Puzzle.move(Direction.DOWN)
        self.assertEqual(Puzzle.state, [3, 1, 2, 4, 5, 8, 6, 7, 0], msg="Did not move the blank tile down.")
        Puzzle.move(Direction.LEFT)
        self.assertEqual(Puzzle.state, [3, 1, 2, 4, 5, 8, 6, 0, 7], msg="Did not move the blank tile left.")
        Puzzle.move(Direction.LEFT)
        self.assertEqual(Puzzle.state, [3, 1, 2, 4, 5, 8, 0, 6, 7], msg="Did not move the blank tile left.")
        Puzzle.move(Direction.UP)
        self.assertEqual(Puzzle.state, [3, 1, 2, 0, 5, 8, 4, 6, 7], msg="Did not move the blank tile up.")
        Puzzle.move(Direction.UP)
        self.assertEqual(Puzzle.state, [0, 1, 2, 3, 5, 8, 4, 6, 7], msg="Did not move the blank tile up.")
        Puzzle.move(Direction.RIGHT)
        self.assertEqual(Puzzle.state, [1, 0, 2, 3, 5, 8, 4, 6, 7], msg="Did not move the blank tile right.")
        Puzzle.move(Direction.RIGHT)
        self.assertEqual(Puzzle.state, [1, 2, 0, 3, 5, 8, 4, 6, 7], msg="Did not move the blank tile right.")

    def test_move_exception(self):
        Puzzle.initialize()
        self.assertRaises(RuntimeError, Puzzle.move, move=Direction.UP)
        self.assertRaises(RuntimeError, Puzzle.move, move=Direction.LEFT)
        Puzzle.move(Direction.RIGHT)
        Puzzle.move(Direction.RIGHT)
        self.assertRaises(RuntimeError, Puzzle.move, move=Direction.UP)
        self.assertRaises(RuntimeError, Puzzle.move, move=Direction.RIGHT)
        Puzzle.move(Direction.DOWN)
        Puzzle.move(Direction.DOWN)
        self.assertRaises(RuntimeError, Puzzle.move, move=Direction.DOWN)
        self.assertRaises(RuntimeError, Puzzle.move, move=Direction.RIGHT)
        Puzzle.move(Direction.LEFT)
        Puzzle.move(Direction.LEFT)
        self.assertRaises(RuntimeError, Puzzle.move, move=Direction.DOWN)
        self.assertRaises(RuntimeError, Puzzle.move, move=Direction.LEFT)
        # Test for invalid move name.
        self.assertRaises(ValueError, Puzzle.move, move="")
        self.assertRaises(ValueError, Puzzle.move, move="down-left")
        self.assertRaises(ValueError, Puzzle.move, move="hello")

    def test_randomize_state(self):
        Puzzle.randomize_state(1)
        self.assertEqual(Puzzle.state, [1, 0] + [i for i in range(2, 9)], msg="Does not shuffle blank tile right.")
        Puzzle.randomize_state(2)
        self.assertEqual(Puzzle.state, [i for i in range(0, 9)], msg="Does not shuffle blank tile left.")
        Puzzle.randomize_state(3)
        self.assertEqual(Puzzle.state, [1, 0] + [i for i in range(2, 9)], msg="Does not shuffle blank tile right.")
        Puzzle.randomize_state(4)
        self.assertEqual(Puzzle.state, [i for i in range(0, 9)], msg="Does not shuffle blank tile left.")
        Puzzle.randomize_state(5)
        self.assertEqual(Puzzle.state, [1, 0] + [i for i in range(2, 9)], msg="Does not shuffle blank tile right.")
        Puzzle.randomize_state(6)
        self.assertEqual(Puzzle.state, [1, 4, 2, 3, 0, 5, 6, 7, 8], msg="Does not shuffle the blank tile down.")

# Run the test.
if __name__ == "__main__":
    unittest.main()