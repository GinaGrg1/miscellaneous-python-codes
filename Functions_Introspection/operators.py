from operator import itemgetter, attrgetter
import operator
from functools import partial, reduce

#getitem(s, i)  # returns s[i]
f = itemgetter(1)  # almost like a partial function. This is a callable.
s = [1, 2, 3, 4]
f(s)  # returns 2

f = itemgetter(1,3)
first, third = f(s)


reduce(lambda x, y: x*y, [1, 2, 3, 4])
# OR
reduce(operator.mul, [1, 2, 3, 4, 5])

my_list = [1,2,3,4]
operator.setitem(my_list, 1, 1000)
my_list


class MyClass:
  def __init__(self):
    self.a = 10
    self.b = 20
    self.c = 30
    
  def test(self, c):
    print('test method running..', c)
  
obj = MyClass()
operator.methodcaller('test',100)(obj)

#property_a = operator.attrgetter('a') # callable
operator.attrgetter('a')(obj)
operator.attrgetter('a', 'b')(obj)

l = [5-10j, 3+3j, 2-100j]
sorted(l, key=operator.attrgetter('real'))

l1 = [(2,3,4), (1,3,5), (6,), (4,100)]
sorted(l1, key=operator.itemgetter(0))







