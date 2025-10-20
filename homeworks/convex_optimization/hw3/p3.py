from utils.instance_utils import *
from utils.solve_utils import *


def main():
    # Get random lp instances
    # instances = generate_lp_instances(5)
    instances = generate_lp_feasible_instances(5)

    # Solve instances
    for i, instance in enumerate(instances):
        solution = solve_max_lp_simplex(instance)
        solution_gp = solve_max_lp_simplex_gurobi(instance)
        print(f"instance {i+1}: Implementation: {solution['objective']}, Gurobi: {solution_gp['objective']}")



if __name__ == '__main__':
    main()