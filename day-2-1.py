import json

keypad = {
    (0, 0): 5,
    (0, 1): 2,
    (0, -1): 8,
    (1, 0): 6,
    (-1, 0): 4,
    (1, 1): 3,
    (1, -1): 9,
    (-1, 1): 1,
    (-1, -1): 7
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
    if updated[0] < -1 or updated[0] > 1 or updated[1] < -1 or updated[1] > 1:
        return current
    else:
        return updated

def test_move():
    current = (0, 0)
    assert move(current, UP) == (0, 1)
    assert move(current, LEFT) == (-1, 0)
    assert move(current, DOWN) == (0, -1)
    assert move(current, RIGHT) == (1, 0)
    assert move(move(current, RIGHT), RIGHT) == (1, 0)
    assert move(move(current, RIGHT), LEFT) == (0, 0)

test_move()

def main():
    with open('day-2-input.json') as f:
        instructions = json.load(f)
        current = (0, 0)
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
