class Puzzle:
    """
    A simple struct for holding the puzzle state.

    Class Attributes:
        state (list[int]):
            A list representing the current state of the 8-puzzle.

        valid (bool):
            A boolean value that records the validity of the current puzzle
            state. This entails that all values in the range [0, 8] are present
            in the puzzle and the length of the state is exactly 9 elements.
    """
    
    state: list[int] = []
    valid: bool = False

    def action(command: str) -> None:
        """
        A function to map a command string to a corresponding puzzle function.
        
        Parameters:
            command (str):
                A string representing a command to execute on this puzzle.
        """

        # Remove whitespace and standardize command string.
        args: list[str] = command.lower().strip().split()

        if "setstate" in args[0]:
            # args = ["setstate", "xxx", "xxx", "xxx"]
            # Get the puzzle sequence from the command.
            Puzzle.set_state("".join(args[1:]))
        elif "printstate" in args[0]:
            Puzzle.print_state()

    def set_state(state: str) -> None:
        """
        A function to set and validate the state of the puzzle with a new state.

        Parameters: 
            state (str):
                A string representing a state in the form "xxx xxx xxx" where each
                value x is a number from [0, 9).

        Raises:
            ValueError:
                When the given input state does not meet the requirements specified
                in the parameter description.
        """

        # Trim all spaces from the input.
        state: list[int] = [int(number) for number in state.replace(" ", "")]

        # Validate the values of the proposed input state.
        if len(state) != 9:
            Puzzle.valid = False
            raise ValueError("A state with an invalid length was passed to the puzzle.")
        for n in range(9):
            if n not in state:
                Puzzle.valid = False
                raise ValueError(f"A state is missing the number ${n} in the range [0, 8].")
        
        # Update the puzzle state.
        Puzzle.state = state
        Puzzle.valid = True

    def print_state() -> None:
        if Puzzle.valid:
            print(Puzzle.state[0], Puzzle.state[1], Puzzle.state[2])
            print(Puzzle.state[3], Puzzle.state[4], Puzzle.state[5])
            print(Puzzle.state[6], Puzzle.state[7], Puzzle.state[8])

    def _swap(p1: int, p2: int) -> None:
        """
        A function to swap two tiles in the puzzle state.

        Parameters:
            p1 (int):
                The first position to swap.

            p2 (int):
                The second position to swap.

        Raises: 
            IndexError:
                When either position is not in the range [0, 8].
        """

        if Puzzle.valid:
            Puzzle.state[p1], Puzzle.state[p2] = Puzzle.state[p2], Puzzle.state[p1]

    def move(move: str) -> None:
        """
        A function to move the blank tile in the puzzle.

        Parameters:
            move (str):
                A string representing the desired direction of movement for the
                blank tile.

        Raises:
            RuntimeError:
                When the direction of movement is not possible for the blank tile.
            
            ValueError:
                When the given move direction is not understandable (i.e. not "up",
                "down", "left", or "right").
        """

        if Puzzle.valid:
            move: str = move.strip().lower()
            # Get the position of the blank tile.
            b_pos: int = Puzzle.state.index(0)
            match move:
                case "up":
                    if b_pos < 4:
                        raise RuntimeError("It is not possible to move the blank tile up.")
                    Puzzle._swap(b_pos, b_pos-3)
                case "down":
                    if b_pos > 5:
                        raise RuntimeError("It is not possible to move the blank tile down.")
                    Puzzle._swap(b_pos, b_pos+3)
                case "left":
                    if b_pos % 3 == 0:
                        raise RuntimeError("It is not possible to move the blank tile left.")
                    Puzzle._swap(b_pos, b_pos-1)
                case "right":
                    if b_pos % 3 == 2:
                        raise RuntimeError("It is not possible to move the blank tile right.")
                    Puzzle._swap(b_pos, b_pos+1)
                case _:
                    raise ValueError('The move direction is not "up", "down", "left", or "right".')

    def reset_puzzle() -> None:
        """
        A method to reset the state of the puzzle to its default/intitial state.
        """

        Puzzle.state: list[int] = []
        Puzzle.valid: bool = False

# For command line parsing.
import sys

if __name__ == "__main__":
    """
    Reads commands from the file specified in the command line argument.
    """

    # Check for text file argument.
    if len(sys.argv) < 2:
        print("Requires 1 valid file name.")

    # Read commands from the given text file.
    with open(sys.argv[1]) as file:
        for line in file:
            # Do each action in the file.
            Puzzle.action(line)