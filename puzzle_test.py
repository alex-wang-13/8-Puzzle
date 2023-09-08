import unittest

# Import the required class.
from puzzle import Puzzle

class PuzzleTestCase(unittest.TestCase):

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
        # Erroneously accepts a length 9 state argument outside the raneg [0, 8].
        self.assertRaises(ValueError, Puzzle.set_state, state="123456789")
        # Erroneously accepts a length 9 argument with duplicate numbers.
        self.assertRaises(ValueError, Puzzle.set_state, state="011345688")
        # "Erroneously accepts a length 9 argument with one duplicate number.
        self.assertRaises(ValueError, Puzzle.set_state, state="001345689")
        # Erroneously accepts a length 10 argument.
        self.assertRaises(ValueError, Puzzle.set_state, state="0123456789")

# Run the test.
if __name__ == "__main__":
    unittest.main()