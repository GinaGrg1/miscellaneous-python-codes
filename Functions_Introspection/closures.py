from time import perf_counter


# Nested Closures

def incrementer(n):
  def inner(start):  # inner + n is a closure
    current = start
    def inc():  # inc + current + n is a closure
      nonlocal current  # free variable
      current += n
      return current
    return inc
  return inner

fn = incrementer(2)  # returns closure inner()
inc_2 = fn(100)  # returns inc  (current=100, n=2)
# inc_2.__code__.co_freevars  --> ('current', 'n')

inc_2()  # 102  (current=102, n=2)
inc_2()  # 104  (current=104, n=2)
# fn.__code__.co_freevars  -> ('n',)

######################################################################################
def outer():
  count = 0
  
  def inc1():
    nonlocal count
    count += 1
    return count
  
  def inc2():
    nonlocal count
    count += 1
    return count  
  return inc1, inc2

fn1, fn2 = outer()
fn1.__code__.co_freevars, fn2.__code__.co_freevars, fn1.__closure__, fn2.__closure__

# (('count',), ('count',), (<cell at 0x7f2df3e87690: int object at 0xaa6780>,),(<cell at 0x7f2df3e87690: int object at 0xaa6780>,))


class Averager:
  def __init__(self):
    self.numbers = []
    
  def add(self, number):
    self.numbers.append(number)
    total = sum(self.numbers)
    count = len(self.numbers)
    return total / count
  
# Rewriting the class as a closure
def averager():
  numbers = []
  def add(number):
    numbers.append(number)
    total = sum(numbers)
    count = len(numbers)
    return total / count
  return add

def averager_1():
  total, count = 0, 0
  def add(number):
    nonlocal total  # so that when the closure is called another time, it is not reset to 0.
    nonlocal count
    total += number
    count += 1
    return total / count
  return add

a = Averager()
av = averager()  # this is add. av.__closure__
avg = averager_1()


class Timer:
  """
  To make this class a callable, add __call__.
  """
  def __init__(self):
    self.start = perf_counter()
  
  def __call__(self):
    return perf_counter() - self.start
  
t1 = Timer()
t1()
t1()

# Above class as a closure
def timer():
  start = perf_counter()
  sef poll():
    return perf_counter() - start
  return poll

t2 = timer()
t2()
t2()
######################################################################################

def counter(initial_value=0):
  def inc(increment=1):
    nonlocal initial_value  # if this is not done, it will error out.
    initial_value += increment
    return initial_value
  return inc

c1 = counter()
c2 = counter(5)

c1()  # gives 1
c2(5) # gives 10.

######################################################################################
