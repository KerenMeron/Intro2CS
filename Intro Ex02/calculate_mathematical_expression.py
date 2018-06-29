#########################################################
# FILE: calculate_mathematical_expression.py
# WRITER: keren meron, keren.meron, 200039626
# EXERCISE: intro2cs ex2 2015-2016
# DESCRIPTION: Takes a mathematical expression
#              (once from variabes and once from string)
#              and calculates the result.
#########################################################

ADDITION = '+'
SUBTRACTION = '-'
DIVISION = '/'
MULTIPLICATION = '*'

def calculate_mathematical_expression(num1, num2, operation):
    '''
    Calculates a math expression defined by two numbers and a math operation.
    Calculates the expression and returns the result.
    Optional operations: addition, subtraction, division and multiplication.
    num1, num2 = Accepts two numbers from user.
    operations = Given by user. Performs mathematical operation on
    the two given numbers.
    Returns the result of the calculation.
    '''

    if operation == ADDITION:
        return num1 + num2
    elif operation == SUBTRACTION:
        return num1-num2
    elif operation == MULTIPLICATION:
        return num1 * num2
    elif operation == DIVISION:
        if num2 == 0: #division by zero illegal
            return None
        else:
            return num1 / num2
    else: #illegal mathematical operation
        return None


def calculate_from_string(math_string):
    '''Accepts a string containing a math expression,
    and calculates the result using the
    calculate_mathematical_expression functions.
    Returns the result.'''

    math_list = math_string.split()
    num1 = float(math_list[0])
    num2 = float(math_list[2])
    operation = math_list[1]
    return calculate_mathematical_expression(num1, num2, operation)

