from utils.instance_utils import *
from utils.solve_utils import *


def main():
    # Get instance
    instance = get_ordering_instance()

    # Solve ordering
    order = solve_ordering(instance)
    print(f"Optimal order: {order}")


if __name__ == "__main__":
    main()