import re
from operator import itemgetter
import json

def count_letters_in_order(word):
    d = {}
    for letter in word:
        if letter in d:
            d[letter] += 1
        else:
            d[letter] = 1
    return d

def test_count_letter():
    print('testing test_count_letter')
    d = count_letters_in_order('aaaaa-bbb-z-y-x')
    try:
        assert d['a'] == 5
        assert d['b'] == 3
        assert d['z'] == 1
        assert d['y'] == 1
        assert d['x'] == 1
        assert d['-'] == 4
        d = count_letters_in_order('notarealroom')
        assert d['n'] == 1
        assert d['o'] == 3
        assert d['t'] == 1
        assert d['a'] == 2
        assert d['r'] == 2
        assert d['e'] == 1
        assert d['l'] == 1
        assert d['m'] == 1
    except AssertionError:
        print('Wrong return')
        print(d)

def only_word(word):
    w = word[:-7]
    w = w.replace('-', '')
    return re.search('[a-zA-Z]+', w).group(0)

def test_only_word():
    print('testing only_word')
    assert only_word('aaaaa-bbb-z-y-x-123[abxyz]') == 'aaaaabbbzyx'
    assert only_word('a-b-c-d-e-f-g-h-987[abcde]') == 'abcdefgh'
    assert only_word('not-a-real-room-404[oarel]') == 'notarealroom'
    assert only_word('totally-real-room-200[decoy]') == 'totallyrealroom'

def only_sector_id(word):
    return int(re.search('[0-9]+', word).group(0))

def test_only_sector_id():
    print('testing only_sector_id')
    assert only_sector_id('aaaaa-bbb-z-y-x-123[abxyz]') == 123
    assert only_sector_id('a-b-c-d-e-f-g-h-987[abcde]') == 987
    assert only_sector_id('not-a-real-room-404[oarel]') == 404
    assert only_sector_id('totally-real-room-200[decoy]') == 200

def only_check_sum(word):
    return word[-6:-1]

def test_only_check_sum():
    print('testing only_check_sum')
    assert only_check_sum('aaaaa-bbb-z-y-x-123[abxyz]') == 'abxyz'
    assert only_check_sum('a-b-c-d-e-f-g-h-987[abcde]') == 'abcde'
    assert only_check_sum('not-a-real-room-404[oarel]') == 'oarel'
    assert only_check_sum('totally-real-room-200[decoy]') == 'decoy'

def is_real_room(room):
    word = only_word(room)
    letters_counted = list(count_letters_in_order(word).items())
    sorted_letters = sorted(letters_counted, key=itemgetter(0))
    sorted_letters = sorted(sorted_letters, key=itemgetter(1), reverse=True)
    real_check_sum = ''.join(l[0] for l in sorted_letters[:5])
    check_sum = only_check_sum(room)

    return real_check_sum == check_sum

def test_is_real_room():
    print('testing is_real_room')
    assert is_real_room('aaaaa-bbb-z-y-x-123[abxyz]') == True
    assert is_real_room('a-b-c-d-e-f-g-h-987[abcde]') == True
    assert is_real_room('not-a-real-room-404[oarel]') == True
    assert is_real_room('totally-real-room-200[decoy]') == False

def only_real_rooms(rooms):
    return list(filter(lambda r: is_real_room(r), rooms))

def test_only_real_rooms():
    print('testing only_real_rooms')
    rooms = [
        'aaaaa-bbb-z-y-x-123[abxyz]',
        'a-b-c-d-e-f-g-h-987[abcde]',
        'not-a-real-room-404[oarel]',
        'totally-real-room-200[decoy]'
    ]
    real_rooms = only_real_rooms(rooms)
    assert real_rooms[0] == 'aaaaa-bbb-z-y-x-123[abxyz]'
    assert real_rooms[1] == 'a-b-c-d-e-f-g-h-987[abcde]'
    assert real_rooms[2] == 'not-a-real-room-404[oarel]'
    assert 'totally-real-room-200[decoy]' not in real_rooms

def sum_rooms_selectors_id(rooms):
    return sum([only_sector_id(r) for r in rooms])

def test_sum_rooms_selectors_id():
    print('testing sum_rooms_selectors_id')
    rooms = [
        'aaaaa-bbb-z-y-x-123[abxyz]',
        'a-b-c-d-e-f-g-h-987[abcde]',
        'not-a-real-room-404[oarel]',
        'totally-real-room-200[decoy]'
    ]
    total = sum_rooms_selectors_id(rooms)
    assert total == 1714

def main():
    with open('day-4-input.json') as f:
        data = json.load(f)
        rooms = only_real_rooms(data)
        print(sum_rooms_selectors_id(rooms))

test_count_letter()
test_only_word()
test_only_sector_id()
test_only_check_sum()
test_is_real_room()
test_only_real_rooms()
test_sum_rooms_selectors_id()

if __name__ == '__main__':
    main()
