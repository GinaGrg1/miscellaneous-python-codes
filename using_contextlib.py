from contextlib import closing


class RefrigeratorRaider:
    """ Raid a refrigerator. """

    def open(self):
        print("Open the fridge door.")
    
    def take(self, food):
        print("Finding {}....".format(food))
        if food == "deep fried pizza":
            raise RuntimeError("Health warning!!")
        print("Taking {}".format(food))
    
    def close(self):
        print("Closing the fridge door.")


def raid(food):
    with closing(RefrigeratorRaider()) as r:  # closing() has a builtin close() method which is called in the end. This close() method MUST be present else it will error out.
        r.open()
        r.take(food)

