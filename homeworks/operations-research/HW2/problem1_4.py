from utils.instance_utils import *
from utils.solve_utils import *


def main():
    number_of_instances = 1
    # number_of_instances = 5
    dim = 10
    # get instances as model input
    instances = generate_instances(number_of_instances, dim)

    # solve every instance using each method
    for Q, A, c, b in instances:
        x1, u1 = analytical_solver(Q, A, c, b, dim)
        x2, u2 = gradient_descent_solver(Q, A, c, b, dim)

        # print results for each solver
        print(f"x: \n{x1.T}, \n{x2.T}\n")
        print(f"u: \n{u1.T}, \n{u2.T}\n")


if __name__ == "__main__":
    main()