from utils.instance_utils import *
from utils.solve_p2_utils import *
import time


def main():
    # get instance for solving methods
    a, c, d = generate_p2_instance()

    # get start time
    time0 = time.time()

    # solve the problem using each method
    MasSubModel = MasterSubproblemModel()
    x1 = MasSubModel.solve()
    time1 = time.time()
    time2 = time.time()

    # get running time of each solver
    running_time1 = time1 - time0
    running_time2 = time2 - time1
    
    # print results for each solver
    print(f"running time: \n{running_time1}, \n{running_time2}\n")
    print(f"Optimal Solution: x = {x1}")


if __name__ == "__main__":
    main()