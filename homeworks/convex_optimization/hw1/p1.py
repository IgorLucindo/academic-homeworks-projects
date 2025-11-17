from utils.instance_utils import *
from utils.solve_utils import *


def main():
    # Get instance
    instance = get_max_balance_instance()

    # Solve shipping
    solution = solve_max_balance(instance)

    # Print
    print(
        f"\nObjVal: {solution['objval']}"
        f"\nX: {solution['x']}"
        f"\nY: {solution['y']}"
    )


if __name__ == "__main__":
    main()