import unittest


def digits(x):
    """
    Convert an integer into a list of digits.
    :param x: The number whose digits we want.
    :return: A list of the digits, in order, of ``x``.

    digits(4586378)
    [4,5,8,6,3,7,8]
    """
    #import pdb; pdb.set_trace()  # this can be used to stop program execution & enter the debugger.

    digs = []
    while x != 0:
        div, mod = divmod(x, 10)  # returns (x//y, x%y)
        digs.append(mod)
        x = div
    return digs


def is_palindrome(x):
    """
    Determine if an integer is an palindrome.
    :param x: Number to check if it is palindrome.
    :return: True if palindrome, else False.
    """
    digs = digits(x)
    for f, r in zip(digs, reversed(digs)):
        if f != r:
            return False
    return True


class Tests(unittest.TestCase):
    """ Tests for the ``is_palindrome()`` function."""
    def test_negative(self):
        " Check that it returns False correctly."
        self.assertFalse(is_palindrome(1234))

    def test_positive(self):
        " Check that it returns True correctly."
        self.assertTrue(is_palindrome(1234321))

    def test_single_digit(self):
        " Check that it works for single digit numbers."
        for i in range(10):
            self.assertTrue(is_palindrome(i))


if __name__ == '__main__':
    unittest.main()