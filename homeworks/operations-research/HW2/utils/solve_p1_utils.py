import numpy as np
from scipy.optimize import minimize


# solve analyticaly from KKT Conditions method
def analytical_solver(Q, A, c, b):
    Q_inv = np.linalg.inv(Q)
    # getting u
    u = -np.linalg.inv(A @ Q_inv @ A.T)@(b + A@Q_inv@c)

    # get value of x based on u
    x = -Q_inv@(c + A.T@u)

    # objective function value
    value = 0.5*x.T@Q@x + c.T@x

    # return variables x and u
    return x, u, value.item()


# solve by gradient descent from Lagrangian Duality method
def gradient_descent_solver(Q, A, c, b):
    c = c.flatten()
    b = b.flatten()

    # precompute fixed terms
    Q_inv = np.linalg.inv(Q)
    g = A@Q_inv@A.T
    h = A@Q_inv@c + b
    l = 0.5*c.T@Q_inv@c
    function = lambda u: 0.5*np.dot(g@u, u) + np.dot(u, h) + l
    gradient = lambda u: g@u + h

    # gradient descent
    res = minimize(fun=function, x0=np.zeros(A.shape[0]), jac=gradient, method='BFGS')
    u = res.x

    # get value of x based on u
    x = -Q_inv@(c + A.T@u)

    # objective function value
    value = 0.5*np.dot(x, Q@x) + np.dot(c, x)

    # return variables x and u
    return x, u, value


# solve by newton's method from Lagrangian Duality method
def newton_method_solver(Q, A, c, b, tol=1e-6, max_iter=1000):
    # precompute fixed terms
    Q_inv = np.linalg.inv(Q)
    g = A@Q_inv@A.T
    h = A@Q_inv@c + b
    gradient = lambda u: g@u + h
    H_inv = np.linalg.inv(g)

    # newton's method
    u = np.zeros((A.shape[0], 1))
    for i in range(max_iter):
        delta = H_inv @ gradient(u)
        u -= delta
        if np.linalg.norm(delta) < tol:
            break

    # get value of x based on u
    x = -Q_inv@(c + A.T@u)

    # objective function value
    value = 0.5*x.T@Q@x + c.T@x

    # return variables x and u
    return x, u, value.item()


# solve the linear system from KKT Conditions method
def linear_system_solver(Q, A, c, b):
    dim = A.shape[0]

    # get the linear system
    matrix = np.block([[Q, A.T],
                       [A, np.zeros((dim, dim))]])
    vector = np.block([[-c],
                       [b]])

    # solve and get variables vector
    variables = np.linalg.solve(matrix, vector)
    x, u = np.split(variables, [dim])

    # objective function value
    value = 0.5*x.T@Q@x + c.T@x

    # return variables x and u
    return x, u, value.item()