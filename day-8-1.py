commands = [
    'rect 3x2',
    'rotate column x=1 by 1',
    'rotate row y=0 by 4',
    'rotate column x=1 by 1'
]

def matrix(x, y):
    return [['.'] * x for y in range(y)]

def transpose(matrix):
    return [list(m) for m in zip(*matrix)]

def shift(row):
    mirror = [r for r in row]
    for i in range(len(row)):
        row[(i + 1) % len(row)] = mirror[i]
    return row

def shift_by(matrix, index, num, what):
    if what == 'row':
        return shift_row_by(matrix, index, num)
    elif what == 'column':
        return shift_col_by(matrix, index, num)

    raise Exception('non exaustive')


def shift_row_by(matrix, index, num):
    row = matrix[index]
    for _ in range(num):
        row = shift(row)
    matrix[index] = row
    return matrix

def shift_col_by(matrix, index, num):
    matrix = transpose(matrix)
    matrix = shift_row_by(matrix, index, num)
    matrix = transpose(matrix)
    return matrix

def test_shift():
    assert ''.join(shift(list('#..'))) == '.#.'
    assert ''.join(shift(list('..#'))) == '#..'
    assert ''.join(shift(list('..#..'))) == '...#.'

def paint(matrix, x, y):
    for i in range(len(matrix)):
        if i < y:
            for j in range(len(matrix[i])):
                if j < x:
                    matrix[i][j] = '#'
    return matrix

test_shift()

def parse_command(command):
    if command.startswith('rect'):
        return tuple(int(x) for x in command[5:].split('x')) + ('paint',)
    commands = command.split(' ')[1:]
    what = None
    if 'row' == commands[0]:
        what = 'row'
    elif 'column' == commands[0]:
        what = 'column'
    index = int(commands[1][2:])
    num = int(commands[3])

    return index, num, what

def test_parse_command():
    assert parse_command('rect 1x1') == (1, 1, 'paint')
    assert parse_command('rect 3x2') == (3, 2, 'paint')
    assert parse_command('rect 1x5') == (1, 5, 'paint')
    assert parse_command('rect 1x5') == (1, 5, 'paint')
    assert parse_command('rotate row y=0 by 5') == (0, 5, 'row')
    assert parse_command('rotate column x=2 by 3') == (2, 3, 'column')

test_parse_command()

def count_painted(m):
    n = 0
    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] == '#':
                n += 1
    return n

def main():
    from pprint import pprint
    m = matrix(50, 6)
    for c in commands:
        command = (m,) + parse_command(c)
        if command[-1] == 'paint':
            m = paint(*command[:-1])
        else:
            m = shift_by(*command)
    print(count_painted(m))

main()
