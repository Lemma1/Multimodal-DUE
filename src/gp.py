import numpy as np
import cvxopt
from cvxopt import matrix, solvers
cvxopt.solvers.options['show_progress'] = False

def get_projection(q, x):
    # solve min |y-x|_2^2, s.t sum(y) = q, y >= 0
    q = np.float(q)
    if q == 0:
        return np.zeros(x.shape)
    n = len(x)
    lambda_2 = (np.sum(x)  - q) / np.float(n)
    return x - lambda_2
    # n = len(x)
    # min_x = np.min(x)
    # x_sum = np.sum(x)
    # sorted_x = np.sort(x)
    # for i in range(n-1):
    #     lambda_2 = ((x_sum - np.sum(sorted_x[:i])) - q) / np.float(n - i)
    #     if lambda_2 <= min_x:
    #         if i == 0:
    #             thres = -np.inf
    #         else:
    #             thres = sorted_x[i-1]
    #         res = (x - lambda_2)
    #         res[x <= thres] = 0
    #         return res
    # return solve_cvx(q, x)

def solve_cvx(q, x):
    q = np.float(q)
    n = len(x)
    Q = matrix(np.eye(n), (n,n))
    p = matrix(-2 * x, (n, 1))
    G = matrix(-np.eye(n), (n, n))
    h = matrix(np.zeros(n), (n, 1))
    A = matrix(np.ones(n), (1, n))
    b = matrix(q)
    sol = solvers.qp(Q, p, G, h, A, b)
    return np.array(sol['x']).flatten()