####################################################
# FILE: ex3.py
# WRITER: keren meron, keren.meron, 200039626
# EXERCISE: intro2cs ex3 2015-2016
# DESCRIPTION: a set of functions practicing loops
####################################################

def create_list():
    '''
    creates a list of inputs by user, until user enters null
    :return: list, of all inputs by user
    '''

    user_input = ' '
    input_list = list()

    while user_input:
        user_input = input()
        input_list.append(user_input)
    input_list.remove('') #remove last empty input

    return input_list


def concat_list(lst_str):
    '''
    joins strings from a list as one whole string.
    :param lst_str: a list of strings
    :return: a string of the parameters combined
    '''

    concatenation = ''
    for word in lst_str:
        concatenation += word
    return concatenation


def avr(num_list):
    '''
    calculates the average of a list of numbers.
    :param num_list: a list of floats
    :return: the average: sum of the floats divided by the number of floats
    '''

    average = 0
    for num in num_list:
        if num < 0 :
            break
        average += num
    if len(num_list) == 0: #no numbers in input
        average = None
    else:
        average /= len(num_list)

    return average


def permutation(lst, d):
    '''
    preforms a permutation on the list by moving each index forward d spaces.
    the last indexes will move to the beginning of the string.
    formula: index >> ( index + d ) % 2
    :param lst: a list of strings
    :param d: size by which each index is moved
    :return: new list, after trasformation on lst
    '''
    LEN = len(lst)
    new_lst = ['']*LEN

    for i in range(LEN):
        new_lst[(i+d) % LEN] = lst[i]

    return new_lst


def cyclic (lst1, lst2):
    '''
    compares two lists and checks if one is a permutation of the other.
    uses the permutation function,
    and checks it for all d values smaller than the length of the lists.
    :param lst1: list of strings
    :param lst2: list of strings
    :return: True if one list is a permutation of the other, else False.
                Definite False if lists do not match in length.
    '''

    permutation_boolean = True

    if len(lst1) != len(lst2):
        permutation_boolean = False

    if permutation_boolean: #if lists are equal in length

        for d in range (len(lst1)):
            if permutation(lst1, d) == lst2:
                permutation_boolean = True
                break
            else:
                permutation_boolean = False

    return permutation_boolean


def hist(n, list_num):
    '''
    Checks how many times each number in range(n),
    appears in a list of numbers.
    :param list_num: a list of numbers
    :param n: upper limit for numbers checked:
                will check if numbers 0 <= num < n are in list.
    :return: a list: the i-index is the number of times 'num' was in list_num
    '''

    counted = []
    inner_count = 0

    for num in range(n):
        for check in list_num:
            if num == check:
                inner_count += 1
        counted.append(inner_count)
        inner_count = 0

    return counted


def prime_list(num):
    '''
    Returns a list of all prime numbers up to num.
    Logic: Sieve of Eratosthenes: removes multiples of smaller prime numbers
    '''

    primes = list()
    numbers = [True]*num
    numbers[0] == False
    numbers[1] == False

    for i in range(2,num):
        if numbers[i]:
            primes.append(i)
            for multiples in range(i*2, num, i):
                numbers[multiples] = False
    primes.append(num)

    return primes


def fact(n):
    '''
    calculates the prime factors of a positive integer,
    by dividing n by all primes smaller than n (using prime_list function).
    :param n: a positive integer.
    :return: a list of the primary numbers found.
    '''

    n_copy = n
    factors_lst = []
    primes = prime_list(n)

    for divisor in primes:
        while n_copy % divisor == 0:
            n_copy /= divisor
            factors_lst.append(divisor)
        if n_copy == 1:
            break

    return factors_lst


def cart(lst1, lst2):
    '''
    makes lists, each with 2 strings: one from lst1 and the other from lst2.
    finds all the possible combinations.
    :param lst1: list of strings
    :param lst2: list of strings
    :return: a list of nested lists, each with a possible combination
            of strings from the two original lists.
            if lst1/lst2 empty, will return an empty list.
    '''

    cart_list = []
    for string1 in lst1:
        if lst1 == []:
            break
        for string2 in lst2:
            if lst2 == []:
                break
            cart_list.append([string1,string2])

    return cart_list


def pair(n, num_list):
    '''
    finds all the pairs of numbers in num_list, whose sum equals to n.
    :param n: integer
    :param num_list: list of different numbers
    :return: ???????????????????
    '''

    pairs = []
    num_copy = num_list

    for i in num_list:
        num_copy = num_copy[1:]
        for j in num_copy:
            if n == i + j:
                pairs.append([i,j])

    return pairs

