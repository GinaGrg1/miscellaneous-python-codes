"""
Decorators in general:
* takes a function as an argument
* returns a closure
* the closure usually accepts any combination of parameters
* runs some code in the inner function (closure)
* the closure function calls the original function using the arguments passed to the closure.

* wraps can be used to fix the metadata of our inner function in the decorator.
"""

from functools import wraps

def counter(fn):
  count = 0
  
  @wraps
  def inner(*args, **kwargs):
    nonlocal count
    count += 1
    print("{0} has been called {1} times".format(fn.__name__, count))
    #counters[fn.__name__] = count
    return fn(*args, **kwargs)  # fn is a closure.
  return inner

def add(a, b):
  return a + b

@counter
def mult(a, b):
  return a * b
