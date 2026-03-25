"""Main entry point for maze-generator."""

from typing import TYPE_CHECKING

from maze_generator import generate_maze

if TYPE_CHECKING:
    from maze_generator.maze import Path


def main() -> None:
    """Run the maze generator application."""
    maze = generate_maze(30, 30)
    paths: list[Path] = maze.paths(0, 0, 29, 29)
    print(maze)  # noqa: T201
    print(f"Number of paths from (0, 0) to (29, 29): {len(paths)}")  # noqa: T201
    if paths:
        shortest_path = min(paths, key=len)
        print("Example path:", shortest_path)  # noqa: T201
        print(maze.highlighted_path(shortest_path))  # noqa: T201


if __name__ == "__main__":
    main()
