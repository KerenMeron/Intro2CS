#!/usr/bin/env python3


##################################################################
# FILE: ex11.py
# WRITER: Keren Meron, keren.meron, 200039626
# EXERCISE: intro2cs ex11 2015-2016
# DESCRIPTION: mathemtical functions using 2nd order programming
##################################################################


import math

EPSILON = 1e-5
DELTA = 1e-3
INIT_DELTA = 0.01
SEGMENTS = 100
BOUNDARY = 10000
INIT_BOUNDARY = 5

def plot_func(graph, f, x0, x1, num_of_segments=SEGMENTS, c='black'):
    """
    plot f between x0 and x1 using num_of_segments straight lines.
    use the plot_line function in the graph object. 
    f will be plotted to the screen with color c.
    param graph (type Graph): Graphic User Interface object.
    param f(function): a mathematical function.
    param x0(int): left boundary of function.
    param x1(int): right boundary of function.
    param num_of_segments(int): segments to draw as straight lines which will
                                form a graph.
    param c(str): color to draw graph in.
    """

    seg_width = (abs(x0) + abs(x1)) / num_of_segments
    for seg in range(num_of_segments):

        x_first = x0 + seg * seg_width
        x_second = x_first + seg_width
        p1 = (x_first, f()(x_first))
        p2 = (x_second, f()(x_second))

        graph.plot_line(p1, p2, c)


def const_function(c):
    """return the mathematical function f such that f(x) = c"""
    f = lambda x: c
    return f


def identity():
    """return the mathematical function f such that f(x) = x"""
    f = lambda x : x
    return f


def sin_function():
    """return the mathematical function f such that f(x) = sin(x)"""
    f = lambda x : math.sin(x)
    return f


def sum_functions(g, h):
    """return f s.t. f(x) = g(x)+h(x)"""
    f = lambda x : g(x) + h(x)
    return f

def sub_functions(g, h):
    """return f s.t. f(x) = g(x)-h(x)"""
    f = lambda x : g(x) - h(x)
    return f

def mul_functions(g, h):
    """return f s.t. f(x) = g(x)*h(x)"""
    f = lambda x : g(x) * h(x)
    return f

def div_functions(g, h):
    """return f s.t. f(x) = g(x)/h(x)"""
    f = lambda x : g(x) / h(x)
    return f

def derivative(g, delta=DELTA):
    """return f s.t. f(x) = g'(x)"""
    f = lambda x : (g(x+delta) - g(x)) / delta
    return f

def solve(f, x0=-BOUNDARY, x1=BOUNDARY, epsilon=EPSILON):
    """
    Return the solution to f in the range between x0 and x1.
    Assumes f is continuous. Returns None in case of no solution.
    """

    if f(x0)*f(x1) <= 0:
        x = (x0 + x1) / 2
        while abs(f(x)) > epsilon:

            if not f(x0):
                return x0
            elif not f(x1):
                return x1

            x = (x0 + x1) / 2
            if f(x)*f(x0) < 0:
                x1 = x
            elif f(x)*f(x1) < 0:
                x0 = x
        return x

    else:
        return None

def solution_direction(f, x):
    """
    returns True if the solution to the function is to the right on the
    x axis of the x0-x1 range, or else if to the left of it.
    assumes f is one-to-one, and that f(x) does not equal 0.
    """

    if f(x) < 0:
        if derivative(f)(x) < 0:
            return False
        else:
            return True
    else:
        if derivative(f)(x) < 0:
            return True
        else:
            return False


    # inverse assumes that g is continuous and monotonic. 
def inverse(g, epsilon=EPSILON):
    """return f s.t. f(g(x)) = x"""

    def f(x):

        h = lambda y : g(y) - x

        x0 = -INIT_BOUNDARY
        x1 = INIT_BOUNDARY

        while solve(h, x0, x1, epsilon) == None:

            if solution_direction(h, x0):
                x0 = x1
                x1 += INIT_BOUNDARY
            else:
                x1 = x0
                x0 -= INIT_BOUNDARY

        return solve(h, x0, x1, epsilon)

    return f


def compose(g, h):
    """return the f which is the compose of g and h """
    f = lambda x : g(h(x))
    return f


def definite_integral(f, x0, x1, num_of_segments=SEGMENTS):
    """return a float - the definite_integral of f between x0 and x1."""

    width = abs((x1 - x0)) / num_of_segments
    riemann_sum = 0
    x1 = x0+width

    for i in range(num_of_segments):
        riemann_sum += f((x0+x1) / 2) * (x1 - x0)
        x0 = x1
        x1 += width

    return riemann_sum


def integral_function(f, delta=INIT_DELTA):
    """return F such that F'(x) = f(x)"""

    def g(x):
        num_segs = math.ceil(abs(x) / delta)

        if x < 0:
            return -definite_integral(f, x, 0, num_segs)
        elif x > 0:
            return definite_integral(f, 0, x, num_segs)
        else:
            return 0

    return g


def ex11_func_list():
    """return a list of functions as a solution to q.12"""
    return [f0, f1, f2, f3, f4, f5, f6, f7]


def f0():
    """returns the function 4."""
    return const_function(4)

def f1():
    """returns the function sin(x) + 4."""
    return sum_functions(sin_function(), const_function(4))

def f2():
    """returns the function sin(x+4)."""
    return compose(sin_function(), lambda  x: x+4)

def f3():
    """return the function sin(x) * (x^2) / 100."""
    x_squared = mul_functions(identity(), identity())
    return mul_functions(sin_function(),
                         div_functions(x_squared, const_function(100)))

def f4():
    """return the function sin(x) /  (cos(x) + 2)."""
    cosxadd2 = sum_functions(derivative(sin_function()), const_function(2))
    return div_functions(sin_function(), cosxadd2)

def f5():
    """return the antiderivative function of (x^2 + x -3)."""
    xminus3 = sum_functions(identity(), const_function(-3))
    f = sum_functions(mul_functions(identity(), identity()), xminus3)
    return integral_function(f)

def f6():
    """return the function 5 * (sin(cos(x)) - cos(x))."""
    cosx = derivative(sin_function())
    sincos_minuscos = sub_functions(compose(sin_function(), cosx), cosx)
    return mul_functions(const_function(5), sincos_minuscos)

def f7():
    """return the inverse function of x^3."""
    x_pow3 = mul_functions(identity(), mul_functions(identity(), identity()))
    return inverse(x_pow3)

# function that generate the figure in the ex description
def example_func(x):
    return (x/5)**3

if __name__ == "__main__":
    import tkinter as tk
    from ex11helper import Graph
    master = tk.Tk()
    graph = Graph(master, -10, -10, 10, 10)
    color_arr = ['black', 'blue', 'red', 'green', 'brown', 'purple',
                 'dodger blue', 'orange']
    for f in ex11_func_list():
        plot_func(graph, f, -10, 10, 1000, 'slate blue')
    master.mainloop()
