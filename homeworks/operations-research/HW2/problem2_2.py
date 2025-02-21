from utils.instance_utils import *
from utils.solve_p2_utils import *
import time


def main():
    # get instance for solving methods
    instance = generate_p2_instance()

    # get start time
    time0 = time.time()

    # solve the problem using each method
    method1 = MasterSubproblemMethod(instance)
    x1, obj_val1, opt_gap1 = method1.solve()
    time1 = time.time()
    time2 = time.time()

    # get running time of each solver
    running_time1 = time1 - time0
    running_time2 = time2 - time1
    
    # print results for each solver
    print(f"\nMaster Subproblem Method:\n Running Time (s): {running_time1:.3f}\n Optimal Solution: x = {x1}\n Objective Function Value: {obj_val1}\n Optimality Gap: {opt_gap1}\n")


if __name__ == "__main__":
    main()