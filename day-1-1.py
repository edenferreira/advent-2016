from collections import namedtuple
import json

North = 'North'
East = 'East'
South = 'South'
West = 'West'
Right = 'R'
Left = 'L'

Coord = namedtuple('Coord', 'x,y,direction')


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
    coord = walk('R53', coord)
    assert (coord.x, coord.y) == (0, -33)
    assert coord.direction.current == West
    coord = walk('R33', coord)
    assert (coord.x, coord.y) == (0, 0)
    assert coord.direction.current == North


def main():
    with open('day-1-input.json') as f:
        instructions = json.load(f)
        initial_coord = Coord(0, 0, Cycle(North, East, South, West))
        coords = [initial_coord]
        for instruction in instructions:
            coords.append(walk(instruction, coords[-1]))
        initial = coords[0]
        last = coords[-1]
        print(blocks_away(initial, last))

test_cycle()
test_coord()

if __name__ == '__main__':
    main()

