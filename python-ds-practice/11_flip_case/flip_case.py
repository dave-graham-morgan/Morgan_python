def flip_case(phrase, to_swap):
    """Flip [to_swap] case each time it appears in phrase.

        >>> flip_case('Aaaahhh', 'a')
        'aAAAhhh'

        >>> flip_case('Aaaahhh', 'A')
        'aAAAhhh'

        >>> flip_case('Aaaahhh', 'h')
        'AaaaHHH'

    """
    new_phrase = []
    for letter in phrase:
        if to_swap.upper() == letter.upper():
            if letter.islower():
                new_phrase.append(letter.upper())
            else:
                new_phrase.append(letter.lower())
        else:
            new_phrase.append(letter)
    return ''.join(new_phrase)

