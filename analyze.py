
def analyze_text(filename):
    """
    Calculate the number of lines and characters in a file.
    :param filename: The name of the file to analyze.
    :raises: IOERROR, if ``filename`` does not exist or can't be read.
    :return: A tuple where the first element is the number of lines in the file & the second element
             is the number of characters.
    """
    lines, chars = 0, 0
    with open(filename, 'rt') as f:
        for line in f:
            lines += 1
            chars += len(line)
        return lines, chars

