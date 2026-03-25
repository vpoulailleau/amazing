"""Maze data structure for maze generator."""


class Maze:
    """Represents a maze with walls between cells.

    The maze includes a hidden row and column of walls to ensure
    the perimeter is always walled.
    """

    def __init__(self, width: int, height: int) -> None:
        """Initialize a maze with given dimensions.

        Args:
            width: Number of cells horizontally
            height: Number of cells vertically
        """
        self.width = width
        self.height = height

        # Initialize walls grid with extra row/column for perimeter
        # walls[row][col] contains wall info for the cell at (row, col)
        self.walls = []
        for row in range(height + 1):  # +1 for hidden row
            self.walls.append([])
            for _ in range(width + 1):  # +1 for hidden column
                # Each cell has top and left walls
                self.walls[row].append({
                    "top": True,  # wall above this cell
                    "left": True,  # wall to the left of this cell
                })
