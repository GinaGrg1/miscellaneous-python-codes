from functools import partial

# partial lets you limit the no of params passed to a func.

def pow(base, exponent):
  return base * exponent

sq = partial(pow, exponent=2)
cube = partial(pow, exponent=3)

# To call
sq(5)  # 5 is the base.

origin = (0,0)
indices = [(1,1), (0,2), (-3,2), (0,0), (10,10)]
distance = lambda a, b: (a[0] - b[0])**2 + (a[1] - b[1])**2

distance((1,1), origin) --> 2

# We want to sort the indices based on its distance from the origin.
f = partial(distance, origin)
sorted(indices, key=f)  # key has to be function which takes ONLY ONE parameter. Hence, we are using partial()
# sorted(indices, key= partial(distance, origin))

[(0,0), (1,1), (0,2), (-3,0), (10,10)]

# Alternately, we could use lambda
f = lambda x: distance(origin, x)
sorted(indices, key=f)
