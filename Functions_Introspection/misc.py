import inspect

# TODO: This is a comment.
def my_func(a: str, b: 'int > 0', *args: 'some extra positional args', 
            k1: 'kw arg1', k2: 'kw arg2' =100, **kwargs: 'some extra keyword args') -> 'something':
  print(a, b, args, k1, k2, kwargs)
  
my_func(1, 2, 3, 4, 5, k1=10, k3= 'happy', k4='go lucky')


ismethod(obj), isfunction(obj), isroutine(obj), 
getcomments(my_func) --> only shows comments immediately preceeding the func. --> will show # TODO: This is a comment.
inspect.signature(my_func) --> inspect.signature(my_func).parameters.values()
inspect.signature(my_func).return_annotation  --> shows what is returned.

inspect.getsource(my_func)

for param in inspect.signature(my_func).parameters.values():
  print('Name :', param.name)
  print('Default :', param.default)
  print('Annotation :', param.annotation)
  print('Kind :', param.kind)
  
  
