def find_factors(num):
    """Find factors of num, in increasing order.

    >>> find_factors(10)
    [1, 2, 5, 10]

    >>> find_factors(11)
    [1, 11]

    >>> find_factors(111)
    [1, 3, 37, 111]

    >>> find_factors(321421)
    [1, 293, 1097, 321421]
    """
    result = []
    for curr_num in range(1, num):
        if num % curr_num == 0:
            if curr_num not in result:
                result.append(int(num / curr_num))
                result.append(curr_num)
    if len(result) == 2:
        return "prime number bitches"
    return result