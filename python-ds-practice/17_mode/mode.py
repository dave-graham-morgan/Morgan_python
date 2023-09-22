def mode(nums):
    """Return most-common number in list.

    For this function, there will always be a single-most-common value;
    you do not need to worry about handling cases where more than one item
    occurs the same number of times.

        >>> mode([1, 2, 1])
        1

        >>> mode([2, 2, 3, 3, 2])
        2
    """
    count = {}
    largest_count = 0
    largest_key = nums[0]
    for num in nums:
        if num in count:
            count[num] = count.get(num) + 1
            if count.get(num) > largest_count:
                largest_count = count.get(num)
                largest_key = num   
        else:
            count[num] = 1
    return largest_key