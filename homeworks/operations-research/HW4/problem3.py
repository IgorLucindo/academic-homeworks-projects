from utils.instance_utils import *
from classes.GridWorld import *


# parameter flags
flags = {
    'plot': True
}


def main():
    # Get grid world
    grid = create_grid_world()

    # Create grid world class
    gw = GridWorld(grid, flags, gamma=0.1)

    # Solve grid world
    gw.solve_grid_world()

    # Show grid world
    gw.show_grid()


if __name__ == "__main__":
    main()