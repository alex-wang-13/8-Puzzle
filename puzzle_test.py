import unittest
import io
import sys

# Import the required class.
from puzzle import Puzzle

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

# Run the test.
if __name__ == "__main__":
    unittest.main()