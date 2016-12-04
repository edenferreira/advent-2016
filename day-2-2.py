import json

keypad = {
    (0, 0): 7,
    (0, 1): 3,
    (0, 2): 1,
    (0, -1): 'B',
    (0, -2): 'D',
    (1, 0): 8,
    (2, 0): 9,
    (-1, 0): 6,
    (-2, 0): 5,

    (1, 1): 4,
    (-1, 1): 2,
    (1, -1): 'C',
    (-1, -1): 'A'
}

UP = 'U'
DOWN = 'D'
RIGHT = 'R'
LEFT = 'L'

def move(current, direction):
    fn = None
    if direction == UP:
        fn = lambda x: (x[0], x[1] + 1)
    elif direction == DOWN:
        fn = lambda x: (x[0], x[1] - 1)
    elif direction == RIGHT:
        fn = lambda x: (x[0] + 1, x[1])
    elif direction == LEFT:
        fn = lambda x: (x[0] - 1, x[1])
    updated = fn(current)
    if updated not in keypad.keys():
        return current
    else:
        return updated

def test_move():
    current = (0, 0)
    assert move(current, UP) == (0, 1)
    assert move(current, LEFT) == (-1, 0)
    assert move(current, DOWN) == (0, -1)
    assert move(current, RIGHT) == (1, 0)
    assert move(move(current, RIGHT), RIGHT) == (2, 0)
    assert move(move(move(current, RIGHT), RIGHT), RIGHT) == (2, 0)
    assert move(move(current, RIGHT), LEFT) == (0, 0)

test_move()

def main():
    with open('day-2-input.json') as f:
        instructions = json.load(f)
        current = (-2, 0)
        result = current
        results = []
        from_keypad = []
        for ins in instructions:
            for i in ins:
                result = move(result, i)
            results.append(result)
            from_keypad.append(keypad[result])
        print(''.join(map(str, from_keypad)))


if __name__ == '__main__':
    main()
