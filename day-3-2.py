import json
from itertools import groupby, chain

def flatten(listOfLists):
    "Flatten one level of nesting"
    return chain.from_iterable(listOfLists)

def is_triangle(a, b, c):
    return a + b > c and b + c > a and c + a > b

def denumerate(l):
    return (v for k, v in l)

def translate(l):
    return zip(*l)

with open('input.json') as f:
    triangles = json.load(f)
    triangles = enumerate(triangles)
    triangles = ((k // 3, v) for k, v in triangles)
    triangles = (v for k, v in groupby(triangles, lambda x: x[0]))
    triangles = (denumerate(x) for x in triangles)
    triangles = (translate(x) for x in triangles)
    triangles = flatten(triangles)
    real = [t for t in triangles if is_triangle(*t)]
    print(len(real))

assert is_triangle(5, 10, 25) == False
assert is_triangle(10, 20, 25) == True
