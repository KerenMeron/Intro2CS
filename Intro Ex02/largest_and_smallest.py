############################################################################
# FILE: largest_and_smallest.py
# WRITER: keren meron, keren.meron, 200039626
# EXERCISE: intro2cs ex2 2015-2016
# DESCRIPTION: Finds the maximum and minimal values out of 3 numbers.
############################################################################

def largest_and_smallest(num1, num2, num3):
    '''Accepts three numbers and returns
    the largest number and the smallest number.'''

    max = num1
    min = num1
    nums_list = [num1, num2, num3]

    for num in nums_list:
        if num > max:
            max = num
        if num < min:
            min = num

    return max, min


