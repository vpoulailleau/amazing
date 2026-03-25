"""Cell data structure for maze walls."""


class Cell:
    """Represents a cell in the maze with wall information.

    Each cell has walls on its top and left sides.
    """

    def __init__(self, *, top: bool = True, left: bool = True) -> None:
        """Initialize a cell with wall states.

        Args:
            top: Whether the wall above this cell exists
            left: Whether the wall to the left of this cell exists
        """
        self.top = top
        self.left = left

    def __eq__(self, other: object) -> bool:
        """Check equality based on wall states.

        Returns:
            True if the cells have the same wall states, False otherwise.
        """
        if not isinstance(other, Cell):
            return NotImplemented
        return self.top == other.top and self.left == other.left

    def __hash__(self) -> int:
        """Return hash based on wall states."""
        return hash((self.top, self.left))

    def __repr__(self) -> str:
        """Return a string representation of the cell."""
        return f"Cell(top={self.top}, left={self.left})"

    def __str__(self) -> str:
        """Return a human-readable string representation."""
        return f"Cell(top={self.top}, left={self.left})"
