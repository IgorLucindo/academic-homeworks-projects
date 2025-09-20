from utils.instance_utils import *
from utils.solve_utils import *


def main():
    # Get instance
    instance = get_sudoku_instance()

    # Solve shipping
    solution = solve_sudoku(instance)

    # Print
    print(
        f"\nX: {solution['x']}"
    )


if __name__ == "__main__":
    main()