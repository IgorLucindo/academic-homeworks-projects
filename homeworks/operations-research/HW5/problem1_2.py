from utils.instance_utils import *
from utils.solve_utils import *


def main():
    # Get instance
    instance = get_shipping_instance()

    # Solve shipping
    shipping = solve_shipping(instance)
    print(f"Shipping: {shipping}")


if __name__ == "__main__":
    main()