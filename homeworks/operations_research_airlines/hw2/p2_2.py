from utils.instance_utils import *
from utils.solve_p2_utils import *


def main():
    # get instance for solving methods
    instance = generate_p2_instance()

    # solve the problem using each method
    # master subproblem method
    method1 = MasterSubproblemMethod(instance)
    x1, obj_val1, running_time1, opt_gap1 = method1.solve()

    # dualization method
    x2, obj_val2, running_time2, opt_gap2 = dualization_solver(instance)

    # print results for each solver
    print(f"\nMaster Subproblem Method:\n Optimal Solution: x = {x1}\n Objective Function Value: {obj_val1}\n Running Time (s): {running_time1:.3f}\n Optimality Gap: {opt_gap1}\n")
    print(f"\nDualization Method:\n Optimal Solution: x = {x2}\n Objective Function Value: {obj_val2}\n Running Time (s): {running_time2:.3f}\n Optimality Gap: {opt_gap2}\n")


if __name__ == "__main__":
    main()