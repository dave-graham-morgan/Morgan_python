def includes(collection, sought, start=None):
    """Is sought in collection, starting at index start?

    Return True/False if sought is in the given collection:
    - lists/strings/sets/tuples: returns True/False if sought present
    - dictionaries: return True/False if *value* of sought in dictionary

    If string/list/tuple and `start` is provided, starts searching only at that
    index. This `start` is ignored for sets/dictionaries, since they aren't
    ordered.

        >>> includes([1, 2, 3], 1)
        True

        >>> includes([1, 2, 3], 1, 2)
        False

        >>> includes("hello", "o")
        True

        >>> includes(('Elmo', 5, 'red'), 'red', 1)
        True

        >>> includes({1, 2, 3}, 1)
        True

        >>> includes({1, 2, 3}, 1, 3)  # "start" ignored for sets!
        True

        >>> includes({"apple": "red", "berry": "blue"}, "blue")
        True
    """
    #first handle the unusual cases of sets and dictionaries
    if isinstance(collection, dict):
        if sought in collection.values():
            return True
        return False
    if isinstance(collection, set):
        if sought in collection:
            return True
        return False
    
    #check to see if start is present
    if start != None:
        for index, item in enumerate(collection):
            if index >= start:
                if item == sought:
                    return True
        return False
    
    #finally there is no start so we start at the beginning
    for item in collection:
        if item == sought:
            return True
    return False


                

