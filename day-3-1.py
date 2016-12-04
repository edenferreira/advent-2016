import json

def is_triangle(a, b, c):
    return a + b > c and b + c > a and c + a > b

with open('day-3-input.json') as f:
    triangles = json.load(f)
    real = [t for t in triangles if is_triangle(*t)]
    print(len(real), len(triangles))

assert is_triangle(5, 10, 25) == False
assert is_triangle(10, 20, 25) == True
