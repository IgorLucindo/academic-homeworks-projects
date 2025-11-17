from utils.instance_utils import *
from utils.solve_utils import *


def main():
    # Get instance
    instance = get_investment_instance()

    # Solve shipping
    solution = solve_investment_benders(instance)

    # Print
    print(
        f"\nObjVal: {solution['objval']:.3}"
        f"\nX: {solution['x']}"
        f"\nTheta: {solution['theta']}"
    )


if __name__ == "__main__":
    main()