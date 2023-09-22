def is_palindrome(phrase):
    """Is phrase a palindrome?

    Return True/False if phrase is a palindrome (same read backwards and
    forwards).

        >>> is_palindrome('tacocat')
        True

        >>> is_palindrome('noon')
        True

        >>> is_palindrome('robert')
        False

    Should ignore capitalization/spaces when deciding:

        >>> is_palindrome('taco cat')
        True

        >>> is_palindrome('Noon')
        True
    """
    cleaned_phrase = [letter.lower() for letter in phrase if letter != ' ']
    reversed = cleaned_phrase.copy()
    reversed.reverse()
    if cleaned_phrase == reversed:
        return True
    else:
        return False