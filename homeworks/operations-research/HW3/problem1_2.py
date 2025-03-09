from utils.solve_utils import *
import time

def main():
    # get start time
    start_time = time.time()

    # solve n queens problem
    solution = solve_n_queens(10)

    # get running time
    running_time = time.time() - start_time

    # print results
    print(f"optimal value: {solution},  running time: {running_time}")


if __name__ == "__main__":
    main()