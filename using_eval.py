import math


def calculation(term):
    """
    For example term can be : sin(rad(90)) or 2 + 5 + 7

    """
    termsdict = {' ': '', '^': '**', '=': '', '?': '', '%': '/100', 'rad': 'radians', 'mod': '%'}
    for key in termsdict.keys():
        term = term.lower().replace(key, termsdict[key])

    func_list = ['sin', 'cos', 'tan', 'cosh', 'sinh', 'tanh', 'sqrt', 'pi', 'radians', 'e']
    for funct in func_list:
        if funct in term:
            term = term.replace(funct, 'math.'+funct)

    try:
        term = eval(term)
    except Exception as exn:
        print("The error is {} : {}. Please try again".format(exn.__class__.__name__, exn))

    return term


def main():
    while True:
        print("\n Welcome to the Scientific calculator. Enter q to exit.")
        inputterm = input("\n What is your calculation? :")

        if inputterm.lower() == 'q':
            exit()
        print(str(calculation(inputterm)))


if __name__ == '__main__':
    main()
