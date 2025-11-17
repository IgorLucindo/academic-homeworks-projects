from utils.instance_utils import *
from utils.solve_utils import *


def main():
    # Get instance
    instance = get_cutting_stock_instance()

    # Solve shipping
    solution = solve_cutting_stock_problem(instance)
    solution_cg = solve_cutting_stock_problem_column_generation(instance)

    # Print
    print(
        f"\nObjVal: {solution['objval']}, ObjValCG: {solution_cg['objval']}"
        f"\nTime: {solution['runtime']:.3}, TimeCG: {solution_cg['runtime']:.3}"
    )


if __name__ == "__main__":
    main()