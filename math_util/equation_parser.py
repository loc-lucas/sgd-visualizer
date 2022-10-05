import math
import multiprocessing
from time import time

import numpy as np
import sympy
from sympy import S, symbols, lambdify
from sympy.parsing.latex import parse_latex
from sympy.parsing.sympy_parser import standard_transformations, parse_expr, \
    implicit_multiplication_application

from math_util.singleton_meta import SingletonMeta


# This should be a class
class EquationParser():
    def __init__(self, func_str=None, symbol_expr=None):
        if func_str is not None:
            self.symbol_expr = self.parse_equation(func_str)
        else:
            self.symbol_expr = symbol_expr
        x, y = symbols("x y")
        self.lambdified_expr = lambdify([x, y], self.symbol_expr, "numpy")

    def parse_equation_latex(self, func_str):
        return parse_latex(func_str).subs('pi', S.Pi).subs('E', sympy.E)

    def parse_equation(self, func_str):
        return parse_expr(func_str, transformations=(standard_transformations + (implicit_multiplication_application,)))

    def evaluate_from_str(self, func_str, x, y):
        func_str = func_str.replace('x', f"({x})").replace('y', f"({y})")
        return self.parse_equation(func_str)

    def evaluate(self, x_val, y_val):
        return self.lambdified_expr(x_val, y_val)

    def get_symbol_expr(self):
        return self.symbol_expr

# def parse_equation(func_str):
#     return parse_expr(func_str, transformations=(standard_transformations + (implicit_multiplication_application,)))
#
# def evaluate_from_str(func_str, x, y):
#     func_str = func_str.replace('x', f"({x})").replace('y', f"({y})")
#     return parse_equation(func_str)
"""
    3 way to calculate vertice z value:
        1. string sub the func_str then evalf -> fastes - 4s for 10000 vertices
        2. np.vectorize() - 8.5s
        3. wrap by callable function then run every iteration -> 9.6s
"""

if __name__ == '__main__':
    s = "x-y"
    # print(evaluate(s, 10, 10))
    # print(evaluate(s, -10, -10))
    # arr = list(zip(range(160000), range(160000)))
    # t = time()
    # with multiprocessing.Pool(processes=4) as pool:
    #     res = pool.map(evaluate, arr)
    # print(time()-t)


    # f = parse_equation(s)
    # t = time()
    # x, y = symbols("x y")
    # arr1 = range(10000)
    # arr1 = np.reshape(arr1, (len(arr1), 1))
    #
    # arr2 = range(10000)
    # arr2 = np.reshape(arr2, (len(arr1), 1))
    #
    # arr = np.concatenate((arr1, arr2), axis=1)
    # lf = lambdify([x, y], f, "numpy")
    # for i in range(1000):
    #     z = lf(*arr[i])
    #     print(z)
    # # for i in range(10000):
    # #     # z = evaluate(s, i, i)
    # #     f.evalf(subs=dict(x=i, y=i))
    #
    # print(time()-t)
