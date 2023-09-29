import heapq
import math
import random

from enum import Enum
from pprint import pprint
from typing import Callable

"""
Bit maps representing the direction the blank tile can move.
For example, VALIDITY_MATRIX[2] = 0b0110 represents the top
right corner of the 8-puzzle, where the blank tile can move
left and down (represented by the set bits in the middle).
"""
VALIDITY_MATRIX = [
    int("0b1100", 2), int("0b1110", 2), int("0b0110", 2),
    int("0b1101", 2), int("0b1111", 2), int("0b0111", 2),
    int("0b1001", 2), int("0b1011", 2), int("0b0011", 2)
]

class Direction(Enum):
    """
    An enum containing the 4 possible directions the blank tiles can move.
    """

    # Bit maps for each value.
    NONE = 0
    UP = int("0b0001", 2)
    LEFT = int("0b0010", 2)
    DOWN = int("0b0100", 2)
    RIGHT = int("0b1000", 2)

class Node:
    """
    A class to represent a Node in the search tree.

    Attributes:
        state_str (str): A string representation of the in-order numbers in this Node.

        b_index (int): An integer representing the index of the blank tile in the puzzle.
    """
    ROWLEN = 3

    def __init__(self,
                 state: list[int] | str,
                 parent: "Node" = None,
                 action: Direction = Direction.NONE,
                 path_cost: int = 0) -> None:
        """
        A constructor for this Node.

        Parameters:
            state (list[int] | str): The state of the puzzle.

            parent (Node): The Node from which this Node was generated (if applicable).

            action (Direction): The action that was performed on the parent Node to generate this Node (if applicable).

            path_cost (int): The total cost of the path from the initial state to this Node.
        """
        
        self.state: list[int] = [int(i) for i in state]
        self.action: Direction = action
        self.parent: Node = parent
        self.path_cost: int = path_cost
        self.state_str: str = "".join([str(n) for n in state])
        self.b_index: int = self.state.index(0)
 
    def __hash__(self):
        """# Convert the state attribute to a hashable representation
        state_hash = tuple(self.state) if isinstance(self.state, list) else self.state

        # Calculate the hash based on state, action, and path_cost
        return hash((state_hash, self.action, self.path_cost))"""
        return hash(self.state_str)

    def __eq__(self, other):
        if isinstance(other, Node):
            """# Compare state, action, and path_cost attributes for equality
            return (self.state == other.state and
                    self.action == other.action and
                    self.path_cost == other.path_cost)"""
            return self.state_str == other.state_str
        return False

    def __lt__(self, other):
        if isinstance(other, Node):
            """# Compare path_cost for less than
            return self.path_cost < other.path_cost"""
            return self.state_str < other.state_str
        raise TypeError("Cannot compare Node with non-Node object")

    def _swap(self, dir: Direction) -> str:
        """
        A function to give the state resulting from a given action on this Node.

        Parameters:
            dir (Direction): The direction to move the blank tile in this puzzle.
        
        Returns:
            Node: The child Node.
        """

        state: list[int] = list(self.state)
        match dir:
            case Direction.UP:
                state[self.b_index], state[self.b_index-3] = state[self.b_index-3], state[self.b_index]
            case Direction.LEFT:
                state[self.b_index], state[self.b_index-1] = state[self.b_index-1], state[self.b_index]
            case Direction.DOWN:
                state[self.b_index], state[self.b_index+3] = state[self.b_index+3], state[self.b_index]
            case Direction.RIGHT:
                state[self.b_index], state[self.b_index+1] = state[self.b_index+1], state[self.b_index]
            case _:
                raise ValueError("Cannot swap in invalid direction.")
        return Node(state, self, dir, self.path_cost + 1)

    def move(self, dir: Direction) -> "Node":
        """
        A function to give the string representation resulting from a given action to this state.

        Parameters:
            dir (Direction): The direction to move the blank tile in this puzzle.
        
        Returns:
            Node: A string representation of the new state.
        """

        if dir.value & VALIDITY_MATRIX[self.b_index]:
            return self._swap(dir)
        else:
            raise ValueError("Invalid move direction for blank tile.")

class Problem:
    def __init__(self,
                 initial: str,
                 goal: str) -> None:
        """
        A constructor for this Problem that defines the initial state and the goal state.

        Parameters:
            initial (str): The starting state of the Problem.

            goal (str): The desired state of the Problem.
        """

        self.initial = initial
        self.goal = goal

    def is_goal(self, state: Node) -> bool:
        """
        A function to check if a given state is the goal state.

        Parameters:
            state (Node): The other Node to check.

        Returns:
            bool: True if the other Node's state string is equal to this one.
        """

        return state.state_str == self.goal

    def expand(self, node: Node = None) -> list[Node]:
        """
        A function to expand the given Node given any Problem.

        Parameters:
            node (Node): The given Node to expand.
        
        Returns:
            list[Node]: A list of Nodes representing the child states of the given Node.
        """

        # An array storing valid direcions.
        d_list: list[Node] = []
        # The index of the blank tile.
        for dir in Direction:
            if VALIDITY_MATRIX[node.b_index] & dir.value:
                d_list.append(dir)

        return [node.move(dir) for dir in d_list]

class Puzzle:
    """
    A struct for holding the puzzle state.

    Class Attributes:
        state (list[int]):
            A list representing the current state of the 8-puzzle.

        is_valid (bool):
            A bool representing the 

        max_nodes (int | float):
            An integer representing the maximium number of Nodes
            to be searched in A* or beam search. Default is math.inf.
    """

    state: list[int] = []
    is_valid: bool = False
    max_nodes: int | float = math.inf

    def action(cmd: str) -> None:
        """
        A function to map a command string to a corresponding puzzle function.
        
        Parameters:
            command (str):
                A string representing a command to execute on this puzzle.
        """

        # Remove whitespace and standardize command string.
        args: list[str] = cmd.lower().strip().split()

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
            problem = Problem(initial="".join(str(i) for i in Puzzle.state), goal="012345678")
            match args[2]:
                case "h1":
                    heuristic = Puzzle.misplaced_tiles
                case "h2":
                    heuristic = Puzzle.manhattan_dist
                case _:
                    print(f"Heuristic (f{args[2]}) not recognized/implemented.")
            Puzzle.solve_astar(problem, heuristic)
        elif "solve" in args[0] and "beam" in args[1]:
            problem = Problem(initial="".join(str(i) for i in Puzzle.state), goal="012345678")
            heuristic = Puzzle.manhattan_dist
            k = int(args[2])
            Puzzle.solve_beam(problem, heuristic, k)
        elif "maxnodes" in args[0]:
            n = int(args[1])
            Puzzle.set_max_nodes(n)
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
            Puzzle.is_valid = False
            raise ValueError("A state with an invalid length was passed to the puzzle.")
        for n in range(9):
            if n not in state:
                Puzzle.is_valid = False
                raise ValueError(f"A state is missing the number ${n} in the range [0, 8].")
        
        # Update the puzzle state.
        Puzzle.state = state
        Puzzle.is_valid = True

    def print_state() -> None:
        if Puzzle.is_valid:
            pprint(" ".join([str(i) for i in Puzzle.state]), width=Node.ROWLEN**2)

    def move(direction: Direction) -> None:
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
                When the given move direction does not exist (i.e. not Direction.UP,
                Direction.DOWN, Direction.LEFT, or Direction.RIGHT).
        """

        # Validate input.
        if (type(direction) is not Direction or
            direction is Direction.NONE):
            raise ValueError("Invalid input argument.")

        # Check is the puzzle state is set.
        if Puzzle.is_valid:
            # Get the index of the blank tile.
            b_index: int = Puzzle.state.index(0)
            if direction.value & VALIDITY_MATRIX[b_index]:
                # Swap blank tile in a given direction.
                Puzzle.__swap(b_index, direction)
            else: 
                raise RuntimeError("Cannot move blank tile in given direction.")
    
    def __swap(b_index: int, direction: Direction) -> None:
        state = Puzzle.state
        match direction:
            case Direction.UP:
                state[b_index], state[b_index-3] = state[b_index-3], state[b_index]
            case Direction.LEFT:
                state[b_index], state[b_index-1] = state[b_index-1], state[b_index]
            case Direction.DOWN:
                state[b_index], state[b_index+3] = state[b_index+3], state[b_index]
            case Direction.RIGHT:
                state[b_index], state[b_index+1] = state[b_index+1], state[b_index]
                
    def randomize_state(n: int) -> None:
        """
        A function to make n random moves from the starting/goal position.
        For consistency, the seed for this function is set to 'axw582'.
        
        Parameters:
            n (int):
                The number of random moves to make.
        """

        # Set seed.
        random.seed("axw582")
        if Puzzle.is_valid:
            # Move n times.
            for _ in range(n):
                # Get a list of valid directions for a given index of blank tile.
                b_index: int = Puzzle.state.index(0)
                d_list: list[Direction] = [d for d in Direction if d.value & VALIDITY_MATRIX[b_index]]
                Puzzle.move(random.choice(d_list))

    def misplaced_tiles(node: Node) -> int:
        """
        A function to count the number of misplaced tiles in the puzzle.

        Parameters:
            node (Node): The node to analyze.

        Returns:
            int: The number of misplaced tiles.
        """

        count = 0
        for i, value in enumerate(node.state):
            if value != i:
                count += 1

        return count

    def manhattan_dist(node: Node) -> int:
        """
        A function to calculate the Manhattan distance for all tiles in the puzzle.

        Parameters:
            node (Node): The node to analyze.

        Returns:
            int: The Manhattan distance of the tiles.
        """

        distance = 0
        for i, value in enumerate(node.state):
            # Get position of index.
            x_i, y_i = i % 3, i // 3
            # Get position of value.
            x_v, y_v = value % 3, value // 3
            # Add the Manhattan distance.
            distance += abs(x_i - x_v) + abs(y_i - y_v)

        return distance

    def solve_astar(problem: Problem, h: Callable[[Node], int]):
        # Define the initial Node.
        node: Node = Node(state=problem.initial)
        # Declare the frontier.
        frontier: list[Node] = []
        heapq.heappush(frontier, (0, node))
        # Track closed states.
        closed_set: set[Node] = set()

        # Store any Node's cheapest cost.
        g_score: dict[Node, int] = dict()
        g_score[node] = 0
        node.path_cost = 0
        # Store any Node's evaluation (i.e. f(n)=g(n)+h(n)), which is the current best guess.
        f_score: dict[Node, int] = dict()
        f_score[node] = h(node) + 0

        # Track the number of Nodes considered.
        n_count: int = 0
        while len(frontier) > 0:
            # Pop the highest priority Node.
            node: Node = heapq.heappop(frontier)[1]
            # Check if the node is closed.
            if node in closed_set:
                continue
            else:
                closed_set.add(node)
            # Check + update the number of Nodes considered.
            if n_count < Puzzle.max_nodes:
                n_count += 1
            else:
                print(f"Exceeded max nodes to consider: {Puzzle.max_nodes}.")
                break

            # Check if the goal has been reached.
            if problem.is_goal(node):
                # TODO Remove print later.
                print("Nodes considered:", n_count)
                return Puzzle.backtrace(node)

            # For each child node of Node.
            for child in problem.expand(node):
                # Add path cost up to child node to the tentative score.
                tentative_score: int = g_score.get(node, math.inf) + 1
                # Check if the path has improved or not.
                if child not in g_score or tentative_score < g_score[child]:
                    # Update tables.
                    child.parent = node
                    g_score[child] = tentative_score
                    f_score[child] = tentative_score + h(child)
                    if child not in frontier:
                        heapq.heappush(frontier, (f_score[child], child))

        return "FAILURE"
    
    def backtrace(node: Node) -> None:
        """
        A function to print out the length of the path from the goal state 
        to the root state and the path itself.

        Parameters:
            node (Node):
                The Node to backtrace back to the root (a Node with no parent).
        """

        # Start with initial empty path.
        path: list[str, str] = []

        # Remap directions from end-to-start to start-to-end.
        remap: dict[str, str] = {
            "up": "down",
            "left": "right",
            "down": "up",
            "right": "left",
            "none": "end"
        }

        # Until we reach the initial Node.
        while node:
            # Add the node + subsequent action.
            path.append((node.state_str, remap[node.action.name.lower()]))
            # Update the current Node.
            node = node.parent

        path = path[:-1]
        # Print the length of the solution path.
        print("d:", len(path))
        for item in path:
            # Print each direction in the solution path.
            print(item[-1])
        return len(path), path

    def solve_beam(problem: Problem, h: Callable[[Node], int], k: int) -> None:
        # Declare the frontier.
        frontier: list[Node] = []
        heapq.heappush(frontier, (0, Node(state=problem.initial)))
        
        # Tracked closed states.
        closed_set: set[Node] = set()

        # Track the number of Nodes considered.
        n_count = 0
        while len(frontier) > 0:
            successors: list[Node] = []
            # Generate the children of nodes in the frontier.
            for node in frontier:
                node: Node = node[1]
                # Check if the node is closed.
                if node in closed_set:
                    continue
                else:
                    closed_set.add(node)

                # Check + update the number of Nodes considered.
                if n_count < Puzzle.max_nodes:
                    n_count += 1
                else:
                    print(f"Exceeded max nodes to consider: {Puzzle.max_nodes}.")
                    return "FAILURE"

                # Check if the goal has been reached.
                if problem.is_goal(node):
                    # TODO Remove print later.
                    print("Nodes considered:", n_count)
                    return Puzzle.backtrace(node)
                
                # Add children of node to successor list.
                for child in problem.expand(node):
                    heapq.heappush(successors, (h(child), child))
            
            # Get the k best successors.
            frontier = heapq.nsmallest(k, successors)

        return "FAILURE"

    def set_max_nodes(n: int | float = math.inf) -> None:
        """
        A function to set the maximum number of Nodes to search.

        Parameters:
            n (int):
                An integer representing the max number of Nodes to search.
        
        Raises:
            ValueError:
                When the input is not a valid number.
        """
        
        if type(n) is int or type(n) is float:
            Puzzle.max_nodes = n
        else:
            raise ValueError(f"Input {n} is not a valid number.")


# For command line parsing.
import sys

# For search timing purposes.
import time
is_timed: bool = False

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
            if "time" in line:
                is_timed = True
            elif "untime" in line:
                is_timed = False
            else:
                if is_timed and "solve" in line:
                    start_time = time.time()
                    Puzzle.action(line)
                    sys.stdout.write("--- %s seconds ---" % (time.time() - start_time) + "\n")
                else:
                    Puzzle.action(line)
                    sys.stdout.write("----------------------------------\n")