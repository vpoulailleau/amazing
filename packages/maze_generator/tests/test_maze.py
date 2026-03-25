"""Tests for maze_generator.maze module."""

from maze_generator.cell import Cell
from maze_generator.maze import CellCoord, Maze, Path


def test_maze_initialization_sets_width_and_height() -> None:
    """Maze should store width and height as public attributes."""
    maze = Maze(width=5, height=3)
    assert maze.width == 5
    assert maze.height == 3


def test_maze_has_walls_attribute() -> None:
    """Maze should have a public walls attribute."""
    maze = Maze(width=2, height=2)
    assert hasattr(maze, "walls")


def test_maze_walls_include_hidden_row_and_column() -> None:
    """Maze walls should include extra row and column for perimeter walls."""
    maze = Maze(width=2, height=2)
    # For a 2x2 maze, we need 3x3 walls (2 cells + 1 hidden per dimension)
    # This will fail initially - that's the red phase of TDD
    assert len(maze.walls) == 3  # width + 1
    assert len(maze.walls[0]) == 3  # height + 1


def test_maze_walls_are_two_types_top_and_left() -> None:
    """Each cell should have top and left wall information."""
    maze = Maze(width=1, height=1)
    # Each position should have both top and left wall data
    # This is a placeholder test - implementation will define the structure
    cell = maze.walls[0][0]
    assert isinstance(cell, Cell)
    assert hasattr(cell, "top")
    assert hasattr(cell, "left")


def test_maze_perimeter_walls_are_present() -> None:
    """All perimeter walls should be present (outer boundary)."""
    maze = Maze(width=2, height=2)
    # Top row should all have top walls
    for col in range(maze.width + 1):
        assert maze.walls[col][0].top is True

    # Left column should all have left walls
    for row in range(maze.height + 1):
        assert maze.walls[0][row].left is True

    # Right column should have left walls (but this is the right edge)
    for row in range(maze.height + 1):
        assert maze.walls[maze.width][row].left is True

    # Bottom row should have top walls
    for col in range(maze.width + 1):
        assert maze.walls[col][maze.height].top is True


def test_paths_is_empty_when_walls_block_path() -> None:
    """Count is zero when there is no open passage."""
    maze = Maze(width=2, height=2)
    assert maze.paths(0, 0, 1, 1) == []


def test_paths_count_simple_open_maze() -> None:
    """Count paths on a fully opened 2x2 maze."""
    maze = Maze(width=2, height=2)
    for y in range(maze.height + 1):
        for x in range(maze.width + 1):
            maze.walls[x][y].top = False
            maze.walls[x][y].left = False

    all_paths = maze.paths(0, 0, 1, 1)
    assert len(all_paths) == 2


def test_paths_start_equals_end() -> None:
    """Start equals end should produce exactly one path."""
    maze = Maze(width=2, height=2)
    all_paths = maze.paths(0, 0, 0, 0)
    assert len(all_paths) == 1
    assert all_paths[0] == Path([CellCoord(0, 0)])


def test_paths_count_simple_maze() -> None:
    """Count paths on a fully opened 3x3 maze."""
    maze = Maze(width=3, height=3)
    for y in range(maze.height + 1):
        for x in range(maze.width + 1):
            maze.walls[x][y].top = False
            maze.walls[x][y].left = False

    all_paths = maze.paths(0, 0, 1, 1)
    assert len(all_paths) == 8


def test_maze_str_representation() -> None:
    """Verify maze ASCII rendering with all boundary walls present."""
    maze = Maze(width=1, height=1)
    maze.walls[0][0].top = True
    maze.walls[0][0].left = True
    maze.walls[0][1].left = True
    maze.walls[1][0].top = True

    expected = "+-+\n| |\n+-+"
    assert str(maze) == expected


def test_paths_count_simple_maze_with_walls() -> None:
    """Count paths on a 3x3 maze with some walls."""
    maze = Maze(width=3, height=3)
    for y in range(maze.height):
        maze.walls[1][y].left = False
        maze.walls[2][y].left = False
    for x in range(maze.width):
        maze.walls[x][1].top = False
        maze.walls[x][2].top = False
    maze.walls[1][1].top = True
    maze.walls[1][2].top = True
    maze.walls[1][1].left = True
    maze.walls[2][1].left = True
    all_paths = maze.paths(0, 0, 2, 2)
    assert len(all_paths) == 2
