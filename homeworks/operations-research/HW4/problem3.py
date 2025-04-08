from utils.instance_utils import *
from utils.solve_utils import *
from utils.results_utils import *


# parameter flags
flags = {
    'plot': False
}


def main():
    # Get grid world
    grid = create_grid_world()

    # Solve grid world
    pi = solve_grid_world(grid)

    show_grid(grid, flags['plot'])


if __name__ == "__main__":
    main()