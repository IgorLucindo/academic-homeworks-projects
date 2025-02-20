import numpy as np


# solve analyticaly from KKT Conditions method
def analytical_solver(Q, A, c, b):
    Q_inv = np.linalg.inv(Q)
    # getting u
    u = -np.linalg.inv(A @ Q_inv @ A.T)@(b + A@Q_inv@c)

    # get value of x based on u
    x = -Q_inv@(c + A.T@u)

    # return variables x and u
    return x, u


# solve by gradient descent from Lagrangian Duality method
def gradient_descent_solver(Q, A, c, b, dim, alpha=0.01, tol=1e-6, max_iter=1000):
    # precompute fixed terms
    Q_inv = np.linalg.inv(Q)
    g = A@Q_inv@A.T
    h = A@Q_inv@c + b
    gradient = lambda u: g@u + h

    # gradient descent
    u = np.zeros((dim, 1))
    for i in range(max_iter):
        delta = alpha * gradient(u)
        u -= delta
        if np.linalg.norm(delta) < tol:
            break

    # get value of x based on u
    x = -Q_inv@(c + A.T@u)

    # return variables x and u
    return x, u


# solve by newton's method from Lagrangian Duality method
def newton_method_solver(Q, A, c, b, dim, tol=1e-6, max_iter=1000):
    # precompute fixed terms
    Q_inv = np.linalg.inv(Q)
    g = A@Q_inv@A.T
    h = A@Q_inv@c + b
    gradient = lambda u: g@u + h
    H_inv = np.linalg.inv(g)

    # newton's method
    u = np.zeros((dim, 1))
    for i in range(max_iter):
        delta = H_inv @ gradient(u)
        u -= delta
        if np.linalg.norm(delta) < tol:
            break

    # get value of x based on u
    x = -Q_inv@(c + A.T@u)

    # return variables x and u
    return x, u


# solve the linear system from KKT Conditions method
def linear_system_solver(Q, A, c, b, dim):
    # get the linear system
    matrix = np.block([[Q, A.T],
                       [A, np.zeros((dim, dim))]])
    vector = np.block([[-c],
                       [b]])

    # solve and get variables vector
    variables = np.linalg.solve(matrix, vector)

    # return variables x and u
    x, u = np.split(variables, [dim])
    return x, u