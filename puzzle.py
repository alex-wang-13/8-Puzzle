import random
from enum import Enum
from typing import Callable

class Direction(Enum):
    UP    = 1
    DOWN  = 2
    LEFT  = 3
    RIGHT = 4

class Node:
    """
    A simple struct that represents a node in the search tree.
    """
    
    def __init__(self, state: list[int], parent: "Node", action: Direction, path_cost: int) -> None:
        """
        A constructor for this struct.

        Parameters:
            state (list[int]):
                A list representing the state represented by this node.

            parent (Node):
                A node from which this node was generated.

            action (Direction):
                An action that was performed on the parent node to reach
                the current state.

            path_cost (int):
                The total cost of the path from the initial state to this
                node.
        """

        self.STATE = state
        self.PARENT = parent
        self.ACTION = action
        self.PATH_COST = path_cost

class Puzzle:
    """
    A struct for holding the puzzle state.

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
    max_depth: int = 0

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
            # Print the current state of the puzzle.
            Puzzle.print_state()
        elif "move" in args[0]:
            # Move the blank tile in the specified direction.
            Puzzle.move(Direction[args[1].upper()])
        elif "randomizestate" in args[0]:
            # Shuffle the puzzle with n moves.
            Puzzle.randomize_state(int(args[1]))
        elif "solve" in args[0] and "a-star" in args[1]:
            heuristic = args[2]
            Puzzle.solve_astar(heuristic)
        elif "solve" in args[0] and "beam" in args[1]:
            k = args[2]
            Puzzle.solve_beam(k)
        elif "maxnodes" in args[0]:
            n = args[1]
            Puzzle.max_nodes(n)
        else:
            print(f"Action (f{args[0]}) not recognized/implemented.")

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

    def move(move: Direction) -> None:
        """
        A function to move the blank tile in the puzzle.

        Parameters:
            move (Direction):
                An integer representing the desired direction of movement for the
                blank tile.

        Raises:
            RuntimeError:
                When the direction of movement is not possible for the blank tile.
            
            ValueError:
                When the given move direction is not understandable (i.e. not Direction.UP,
                Direction.DOWN, Direction.LEFT, or Direction.RIGHT).
        """

        if Puzzle.valid:
            # Get the position of the blank tile.
            b_pos: int = Puzzle.state.index(0)
            match move:
                # TODO idea: Modify logic to use a bitmap.
                case Direction.UP:
                    if b_pos < 3:
                        raise RuntimeError("It is not possible to move the blank tile up.")
                    Puzzle._swap(b_pos, b_pos-3)
                case Direction.DOWN:
                    if b_pos > 5:
                        raise RuntimeError("It is not possible to move the blank tile down.")
                    Puzzle._swap(b_pos, b_pos+3)
                case Direction.LEFT:
                    if b_pos % 3 == 0:
                        raise RuntimeError("It is not possible to move the blank tile left.")
                    Puzzle._swap(b_pos, b_pos-1)
                case Direction.RIGHT:
                    if b_pos % 3 == 2:
                        raise RuntimeError("It is not possible to move the blank tile right.")
                    Puzzle._swap(b_pos, b_pos+1)
                case _:
                    raise ValueError('The move direction is not Direction.UP, Direction.DOWN, Direction.LEFT, or Direction.RIGHT.')

    def randomize_state(n: int) -> None:
        """
        A function to make a random number of steps from the puzzle's initial state.

        Parameters:
            n (int): The number of steps to take from the initial step.
        """
        
        # Re-initialize puzzle before shuffling.
        Puzzle.initialize()
        # Determine the seed.
        random.seed("axw582")
        if Puzzle.valid:
            # Repeat n times.
            for _ in range(n):
                # Search for a valid move.
                searching: bool = True
                while searching:
                    # Choose a random direction.
                    direction: Direction = random.choice(list(Direction))
                    try: 
                        Puzzle.move(direction)
                        searching = False
                    except RuntimeError:
                        pass

    def _astar(h_n: Callable[..., int]):
        pass

    def solve_astar(hueristic: str) -> None:
        match hueristic.lower().strip():
            case "h1":
                h_n: int = len(Puzzle.misplaced_tiles())
            case "h2":
                h_n: int = Puzzle.manhattan_distanxe()
            case _:
                print(f"Hueristic (f{hueristic}) not recognized/implemented.")

    def solve_beam(k: int) -> None:
        pass

    def max_nodes(n: int) -> None:
        """
        A function to set the maximum nodes to be considered during a search.

        Parameters:
            n (int): The maximum nodes to be considered.
        """
        
        Puzzle.max_depth = n

    def initialize() -> None:
        """
        A function to initialize the state of the puzzle to "021 345 678".
        """

        Puzzle.set_state("012345678")

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