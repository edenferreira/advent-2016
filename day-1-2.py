from collections import namedtuple
from functools import partial
from itertools import groupby, chain
import json

def flatten(listOfLists):
    "Flatten one level of nesting"
    return chain.from_iterable(listOfLists)

North = 'North'
East = 'East'
South = 'South'
West = 'West'
Right = 'R'
Left = 'L'
Front = 'F'

def split_instruction(instruction):
    splitted = [instruction[0] + '1']
    amount = int(instruction[1:])
    for _ in range(amount - 1):
        splitted.append('F1')
    return splitted

def test_split_instruction():
    assert split_instruction('R3') == ['R1', 'F1', 'F1']
    assert split_instruction('L5') == ['L1', 'F1', 'F1', 'F1', 'F1']

test_split_instruction()

Coord = namedtuple('Coord', 'x,y,direction')
SimpleCoord = namedtuple('SimpleCoord', 'x,y')

def coord_to_simple(coord):
    return SimpleCoord(coord.x, coord.y)

def coords_to_simple(coords):
    return list(map(coord_to_simple, coords))

class Cycle(object):

    def __init__(self, *args):
        self._current = 0
        self._cycle = args

    def next_in_cycle(self):
        self._current += 1
        if self._current == len(self._cycle):
            self._current = 0
        return self

    def previous_in_cycle(self):
        self._current -= 1
        if self._current == -1:
            self._current = len(self._cycle) - 1
        return self

    @property
    def current(self):
        return self._cycle[self._current]


def decide_direction(instruction, cycle):
    fn = None
    if instruction == Right:
        fn = cycle.next_in_cycle
    elif instruction == Left:
        fn = cycle.previous_in_cycle
    elif instruction == Front:
        fn = lambda: cycle
    else:
        print(instruction)
        raise Exception('non exaustive')
    return fn()


def walk(instruction, coord):
    try:
        direction = decide_direction(instruction[0], coord.direction)
    except:
        print(instruction, coord)
        raise

    amount = int(instruction[1:])
    if direction.current == North:
        return Coord(coord.x, coord.y + amount, direction)
    elif direction.current == East:
        return Coord(coord.x + amount, coord.y, direction)
    if direction.current == South:
        return Coord(coord.x, coord.y - amount, direction)
    elif direction.current == West:
        return Coord(coord.x - amount, coord.y, direction)
    else:
        raise Exception('non exaustive')

def blocks_away(coord_a, coord_b):
    x = coord_a.x - coord_b.x
    y = coord_a.y - coord_b.y
    return abs(x) + abs(y)

def compare(coord_a, coord_b):
    return coord_a.x == coord_b.x and coord_a.y == coord_b.y

def wich_repeats(coords, n = 0):
    first = coords[0]
    rest = coords[1:]
    comp = partial(compare, first)
    found = None
    try:
        found = next(filter(comp, rest))
    except StopIteration:
        return wich_repeats(rest, n + 1)

    return (n, found)


def test_cycle():
    cardinal_directions = Cycle(North, East, South, West)
    assert cardinal_directions.next_in_cycle().current == East
    assert cardinal_directions.next_in_cycle().current == South
    assert cardinal_directions.next_in_cycle().current == West
    assert cardinal_directions.next_in_cycle().current == North
    assert cardinal_directions.previous_in_cycle().current == West
    assert cardinal_directions.previous_in_cycle().current == South
    assert cardinal_directions.previous_in_cycle().current == East


def test_coord():
    initial_coord = Coord(0, 0, Cycle(North, East, South, West))
    coord = walk('R153', initial_coord)
    assert (coord.x, coord.y) == (153, 0)
    assert coord.direction.current == East
    coord = walk('L17', coord)
    assert (coord.x, coord.y) == (153, 17)
    assert coord.direction.current == North
    coord = walk('L100', coord)
    assert (coord.x, coord.y) == (53, 17)
    assert coord.direction.current == West
    coord = walk('L50', coord)
    assert (coord.x, coord.y) == (53, -33)
    assert coord.direction.current == South
    coord = walk('R23', coord)
    assert (coord.x, coord.y) == (30, -33)
    assert coord.direction.current == West
    coord = walk('F30', coord)
    assert (coord.x, coord.y) == (0, -33)
    assert coord.direction.current == West
    coord = walk('R33', coord)
    assert (coord.x, coord.y) == (0, 0)
    assert coord.direction.current == North
    coord = walk('F20', coord)
    assert (coord.x, coord.y) == (0, 20)
    assert coord.direction.current == North


def main():
    with open('day-1-input.json') as f:
        instructions = json.load(f)
        instructions = list(flatten(map(split_instruction, instructions)))
        initial_coord = Coord(0, 0, Cycle(North, East, South, West))
        coords = [initial_coord]
        for instruction in instructions:
            coords.append(walk(instruction, coords[-1]))
        simple_coords = coords_to_simple(coords)
        first = simple_coords[0]

        groups = []
        uniquekeys = []
        data = sorted(enumerate(simple_coords), key=lambda x : x[1])
        for k, g in groupby(data, lambda x : x[1]):
            groups.append(list(g))      # Store group iterator as a list
            uniquekeys.append(k)

        more_than_one = list(flatten(filter(lambda x: len(x) > 1, groups)))

        first_visited_index = min(more_than_one, key=lambda x: x[0])[0]
        first_visited = simple_coords[first_visited_index]

        print(blocks_away(first, first_visited))


test_cycle()
test_coord()

if __name__ == '__main__':
    main()

