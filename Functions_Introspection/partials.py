from functools import partial

# partial lets you limit the no of params passed to a func.

def pow(base, exponent):
  return base * exponent

sq = partial(pow, exponent=2)
cube = partial(pow, exponent=3)

# To call
sq(5)  # 5 is the base.
