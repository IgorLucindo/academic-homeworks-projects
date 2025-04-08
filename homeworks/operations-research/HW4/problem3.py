from utils.instance_utils import *
from classes.gridWorld import *


# parameter flags
flags = {
    'plot': False,
    'plot_iteration': True
}


def main():
    # Get grid world
    grid = create_grid_world()

    # Create grid world class
    gw = GridWorld(grid, flags)

    # Solve grid world
    gw.solve_grid_world()

    # Show grid world
    gw.show_grid(flags['plot'])


if __name__ == "__main__":
    main()