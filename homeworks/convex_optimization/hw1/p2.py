from utils.instance_utils import *
from utils.solve_utils import *


def main():
    # Get instance
    instance = get_min_shipping_cost_instance()

    # Solve shipping
    solution = solve_min_shipping_cost(instance)

    # Print
    print(
        f"\nObjVal: {solution['objval']}"
        f"\nX: {solution['x']}"
    )


if __name__ == "__main__":
    main()