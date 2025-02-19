import numpy as np


def main():
    dim = 10
    # random symmetric matrix
    Q = np.random.rand(dim, dim)
    Q = np.dot(Q, Q.T)

    # random vectors
    c = np.random.rand(dim, 1)


if __name__ == "__main__":
    main()