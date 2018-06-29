#########################################################
# FILE: quadratic_equation.py
# WRITER: keren meron, keren.meron, 200039626
# EXERCISE: intro2cs ex2 2015-2016
# DESCRIPTION: Solves a quadratic equation.
#########################################################

MESSAGE_INPUT_COEFF = "Insert coefficients a,b, and c: "
MESSAGE_ONE_SOLUTION = "The equation has 1 solution:"
MESSAGE_TWO_SOLUTIONS = "The equation has 2 solutions: %s and %s"
MESSAGE_NO_SOLUTIONS = "The equation has no solutions."

def quadratic_equation(a, b, c):
    '''Accepts the coefficients of a quadratic equation,
    and returns the solutions of the equation.
    If there are two solutions, returns both.
    If there is one solution, returns the solution and None.
    If there is no solution, returns None, None.'''

    a = float(a)
    b = float(b)
    c = float(c)
    DISCRIMINANT = b**2 - 4*a*c
    SOLUTION1 = (-b + (DISCRIMINANT ** (1/2))) / 2*a
    SOLUTION2 = (-b - (DISCRIMINANT ** (1/2))) / 2*a
    SOLUTION3 = -b / (2*a) #when there is only 1 result
    solution = (None, None) #base case for 0 results

    if DISCRIMINANT == 0: #1 results
        solution = (SOLUTION3, None)
    elif DISCRIMINANT > 0: #2 results
        solution = (SOLUTION1, SOLUTION2)
        #else: 0 results
    return solution

def quadratic_equation_user_input():
    '''Asks user for three coefficients which form a quadratic equations.
    Solves the equation using the quadratic_equation function.
    Prints the solutions.'''

    coefficients = input(MESSAGE_INPUT_COEFF)
    coefficients = coefficients.split()
    solutions = list(quadratic_equation(coefficients[0],
                                        coefficients[1], coefficients[2]))

    if solutions[1] == None: #1 or 0 results
        if solutions[0] == None: #0 results
            print(MESSAGE_NO_SOLUTIONS)
        else:
            print (MESSAGE_ONE_SOLUTION, solutions[0])
    else: #2 results
        print (MESSAGE_TWO_SOLUTIONS %(solutions[0], solutions[1]))

