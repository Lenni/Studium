from scipy.optimize import minimize
import numpy as np
import matplotlib.pyplot as plt

from sympy import Matrix, pprint, init_printing


def magnet_mat(l, k):
    return Matrix([[1, 0, 0, 0], [l*k, 1, 0, 0], [0, 0, 1, 0], [0, 0, l*k, 1]])


def drift_mat(l):
    return Matrix([[1, l, 0, 0], [0, 1, 0, 0], [0, 0, 1, l], [0, 0, 0, 1]])


def func(x, *args):

    quad_a = magnet_mat(x[0], -0.06)
    quad_b = magnet_mat(x[2], 0.06)
    quad_c = magnet_mat(x[4], -0.06)

    drift_a = drift_mat(x[1])
    drift_b = drift_mat(x[3])
    drift_c = drift_mat(x[5])
    x = args[0]

    y = drift_c* quad_c* drift_b* quad_b* drift_a* quad_a* x

    return y


if __name__ == "__main__":

    init_printing(use_unicode=True)

    #initial_x = Matrix(["a", "b", "c", "d", "e", "f"])
    initial_x = Matrix([10, 1, 10, 1, 10, 1])
    #particle = Matrix(["x", "v_x", "y", "v_y"])
    particle = np.array([1, 0, 0, 0])

    optimizeable = lambda x: func(x, Matrix(["x", "a", "y", "b"]))

    res = minimize(func,args=particle, x0=initial_x, method='Nelder-Mead', tol=1e-6)

    #print(res)

    pprint(func(initial_x, particze))