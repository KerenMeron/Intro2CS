#######################################################
# FILE: ex7.py
# WRITER: Keren Meron, keren.meron, 200039626
# EXERCISE: intro2cs ex7 2015-2016
# DESCRIPTION: exercise practising recursive function
########################################################

MIN_GCD = 1
MIN_PRIME = 3
BIN_ZERO = '0'
BIN_ONE = '1'


#1
def print_to_n(n):
    '''Prints all integers from 1 to n (param int) in ascending order.'''

    if n < 1:
        return None
    elif n == 1:  #base case
        print(1)
    else:
        print_to_n(n-1)
        print(n)

#2
def print_reversed_n(n):
    '''Prints all integers from 1 to n (param int) in descending order.'''

    if n < 1:
        return None
    elif n != 1:
        print(n)
        print_reversed_n(n-1)
    else:
        print (1)  #base case

#3
def is_prime(n):
    '''Returns True if n is a prime number, or false if not.'''
    if n <= 1:
        return False
    if has_divisor_smaller_than(n, n) is True:
        return False
    else:
        return True

#3 helper
def has_divisor_smaller_than(n, i):
    '''Recursive helper function for is_prime().
    Returns True if n has a divisor (not 1) smaller than i, else False.'''

    if n <= MIN_PRIME or i <= 1:
        return False
    elif n != i and n % i == 0:  #base case, found divisor
        return True
    elif has_divisor_smaller_than(n, i-1) is True:
            return True
    else:
        return False

#4
def divisors(n):
    '''Returns a list of all positive integers that divide n without a
    remainder, in ascending order.'''

    if n < 0:
        n *= -1
    if n == 0:
        return []
    else:
        return divisors_helper(n, n)

#4 helper
def divisors_helper(n, x):
    '''Recursive helper function for divisors().
    Returns a list of all positive integers that divide n without a
    remainder, in ascending order.'''

    if x == MIN_GCD:  #base case
        return [MIN_GCD]
    div_lst = divisors_helper(n, x-1)

    if n % x == 0:
        div_lst.append(x)

    return div_lst

#5
def exp_n_x(n, x):
    '''Returns the value (float) exp(x), calculated by its taylor
    series up to n (positive int) variables.'''

    if n == 0:  #base case
        return 1
    elif n < 0:
        return 1 / exp_taylor_helper(n, x)

    return exp_taylor_helper(n, x)

#5 helper1
def factorial(i):
    '''Returns the factorial i! = i*(i-1)*(i-2)*...*2*1'''

    if i == 0:
        return 1
    else:
        return i*factorial(i-1)

#5 helper2
def exp_taylor_helper(n, x):
    '''Recursive helper function for exp_n_x().
    Returns the value (float) exp(x), calculated by its taylor
    series up to n (positive int) variables.'''

    if n == 0:  #base case
        return 1

    sum = (x**n) / factorial(n)
    return sum + exp_taylor_helper(n-1, x)

#6
def play_hanoi(hanoi, n, src, dest, temp):
    '''
    Solves the tower of hanoi puzzle. Consists of n disks in ascending size
    order on one of three rods in a set. Moves all disks in same order to
    another rod.
    Rules: only one disk can be moved at a time, no disk may be placed on a
    smaller disk, and in each move takes the upper disk and placing on a
    different rod.
    :param hanoi: object, the graphic game.
    :param n: int, number of disks in game.
    :param src: object, the rod from which the function will remove disks.
    :param dest: object, the rod to which the function will move disks to.
    :param temp:object, the third rod.
    '''

    if n <= 0:
        pass
    elif n == 1:
        hanoi.move(src, dest)  #base case
    else:
        play_hanoi(hanoi, n-1, src, temp, dest)
        hanoi.move(src, dest)
        play_hanoi(hanoi, n-1, temp, dest, src)

#7
def print_binary_sequences(n):
    '''Prints all possible combinations of 0 and 1, at length of n(int).'''

    if n == 0:
        print('')
        return
    else:
        print_binary_seq_with_prefix(BIN_ZERO, n)
        print_binary_seq_with_prefix(BIN_ONE, n)

#7 helper prefix
def print_binary_seq_with_prefix(prefix, n):
    '''Recursive helper function for print_binary_sequences().
    Prints all possible combinations at length of n (int), of 0 and 1.'''

    if n == 1:  #base case
        print(prefix)
        return

    print_binary_seq_with_prefix(prefix + BIN_ZERO, n-1)
    print_binary_seq_with_prefix(prefix + BIN_ONE, n-1)

#8
def print_sequences(char_list, n):
    '''Prints all possible combinations of length n (int) of the letters
    in char_list (list)'''

    if n == 0:
        print('')
        return

    for prefix in char_list:
        print_sequences_prefix(char_list, n, prefix)

#8,9 helper prefix
def print_sequences_prefix(char_list, n, prefix):
    '''Recursive helper function for print_sequences() and
    for print_no_repetition_sequences_prefix().
    Prints all possible combinations of length n (int) of the letters
    in char_list (list).'''

    for char in char_list:
        if n == 1:  #base case
            print(prefix)
            return

        print_sequences_prefix(char_list, n-1, prefix+char)


#9
def print_no_repetition_sequences(char_list, n):
    '''Prints all combinations with length n (int) of letters from
    char_list (list), without any letter repetitions.'''

    if n == 0:
        print('')
        return

    for prefix in char_list:
        print_no_repetition_sequences_prefix(char_list, n, prefix)

#9 helper
def print_no_repetition_sequences_prefix(char_list, n, prefix):
    '''
    Helper function for print_no_repetition_sequences().
    Prints all combinations at length n (int) of letters from
    char_list (list), starting with the letter 'prefix' (char).
    The combination must be without letter repetition.
    '''

    for char in char_list:
        if n == 1:  #base case
            print(prefix)
            return

        if char not in prefix:
            print_sequences_prefix(char_list, n-1, prefix+char)


#10
def no_repetition_sequences_list(char_list, n):
    '''
    Returns a list of all combinations at list n of letters from char_list,
    without any letter repetitions.
    :param char_list: list of letters.
    :param n: length of wanted combination.
    :return: list of strings (all combinations).
    '''

    if n == 0:
        return ['']

    seq_list = []
    for prefix in char_list:
        seq_list.append(no_repetition_sequences_list_prefix(char_list,
                                                            n, prefix, []))
    new_seq_list = [seq for lst in seq_list for seq in lst]

    return new_seq_list



#10 helper prefix
def no_repetition_sequences_list_prefix(char_list, n, prefix, prefix_list):
    '''
    Recursive helper function for no_repetition_sequences_list().
    Returns a list of all combinations at list n of letters from char_list,
    without any letter repetitions.
    :param char_list: list of letters.
    :param n: length of wanted combination.
    :return: list of strings (all combinations).
    '''

    for char in char_list:

        if n == 1:  #base case
            prefix_list.append(prefix)
            return prefix_list

        if char not in prefix:
            final_lst = no_repetition_sequences_list_prefix\
                            (char_list, n-1, prefix+char, prefix_list)

    return final_lst
