from utils.instance_utils import *
from utils.solve_p1_utils import *
import time


def main():
    number_of_instances = 1
    # number_of_instances = 5
    dim = 10
    # get instances as model input
    instances = generate_p1_instances(number_of_instances, dim)

    # solve every instance using each method
    for Q, A, c, b in instances:
        # get start time
        time0 = time.time()

        # run each solver
        x1, u1, value1 = analytical_solver(Q, A, c, b)
        time1 = time.time()
        x2, u2, value2 = gradient_descent_solver(Q, A, c, b)
        time2 = time.time()
        x3, u3, value3 = newton_method_solver(Q, A, c, b)
        time3 = time.time()
        x4, u4, value4 = linear_system_solver(Q, A, c, b)
        time4 = time.time()

        # get running time of each solver
        running_time1 = time1 - time0
        running_time2 = time2 - time1
        running_time3 = time3 - time2
        running_time4 = time4 - time3

        # print results for each solver
        print(f"optimal value: {value1:.5f}, {value2:.5f}, {value3:.5f}, {value4:.5f}\n")
        print(f"running time: {running_time1:.5f}, {running_time2:.5f}, {running_time3:.5f}, {running_time4:.5f}\n")
        # print(f"x: \n{x1.T}, \n{x2.T}, \n{x3.T}, \n{x4.T}\n")
        # print(f"u: \n{u1.T}, \n{u2.T}, \n{u3.T}, \n{u4.T}\n")


if __name__ == "__main__":
    main()