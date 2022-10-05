import multiprocessing

import numpy as np
import sympy

from math_util.equation_parser import EquationParser
from math_util.singleton_meta import SingletonMeta


# should it be singleton?
class SGDOptimizer():
    def __init__(self, equation_parser):
        self.equation_parser = equation_parser
        self.gradient = self.form_gradient()

    # TODO: apply lambdify to this process to improve performance
    def form_gradient(self):
        x, y = sympy.symbols('x y')
        x_diff = sympy.diff(self.equation_parser.get_symbol_expr(), x)
        y_diff = sympy.diff(self.equation_parser.get_symbol_expr(), y)
        x_diff_parser = EquationParser(symbol_expr=x_diff)
        y_diff_parser = EquationParser(symbol_expr=y_diff)

        def foo(p):
            return np.array([
                x_diff_parser.evaluate(*p),
                y_diff_parser.evaluate(*p)
            ], dtype=np.float32)
        return foo

    def has_converged(self, theta_new, tol):
        return np.linalg.norm(self.gradient(theta_new))/len(theta_new) < tol

    def gradient_descent_with_momentum(self, start, learn_rate, max_iter, gamma=0.00, tol=0.0001):
        steps = [np.array([*start, self.equation_parser.evaluate(*start)], dtype=np.float32)]
        p = start
        v_old = np.zeros_like(p)
        for _ in range(max_iter):
            diff = gamma*v_old + learn_rate * self.gradient(p)
            p = p - diff
            if self.has_converged(p, tol):
                break
            v_old = diff
            point = [*p, self.equation_parser.evaluate(*p)]
            steps.append(point)

        # partition = int(len(steps)/4)
        # need to pass func_str into the parallel data because we cannot access instance method of singleton class in multiprocessing progress
        # data_lst = [
        #     [steps[0: partition], func_str],
        #     [steps[partition: partition*2], func_str],
        #     [steps[partition*2: partition*3], func_str],
        #     [steps[partition*3: ], func_str]
        # ]
        # with multiprocessing.Pool() as pool:
        #     z = pool.map(self._parallel_eval, data_lst)
        # z = np.concatenate(z, axis=0)
        # steps = np.concatenate((steps, np.transpose([z])), axis=1)
        return steps, p

    def _parallel_eval(self, data):
        z = []
        steps = data[0]
        func_str = data[1]
        for i in range(len(steps)):
            z += [self.equation_parser.evaluate(steps[i][0], steps[i][0])]
        return z

if __name__ == '__main__':
    # str = "x**2 + y**2 + sin(x*y)"
    # f = parse_expr(str)
    # sgd = SGDOptimizer(f)
    print('test')

