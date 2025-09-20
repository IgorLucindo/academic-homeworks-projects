from utils.instance_utils import *
from utils.solve_utils import *


def main():
    num_samples = [1e1, 1e2, 1e3]

    for i in range(len(num_samples)):
        # Get instance
        instance = get_shipping_instance(num_samples[i])

        # Solve shipping
        shipping = solve_shipping(instance)
        print(f"Case {i+1}  Shipping: {shipping}")


if __name__ == "__main__":
    main()