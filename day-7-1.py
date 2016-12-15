data = [
  'abba[mnop]qrst',
  'abcd[bddb]xyyx',
  'aaaa[qwer]tyui',
  'ioxxoj[asdfgh]zxcvbnioxxoj[asdfgh]zxcvbn'
]

def split_word(word):
    outside = []
    inside = []
    temp = ''
    for w in word:
        if w == '[':
            outside.append(temp)
            temp = ''
        elif w == ']':
            inside.append(temp)
            temp = ''
        else:
            temp += w
    outside.append(temp)
    return (outside, inside)

def test_split_word():
    print(split_word('abba[mnop]qrst'))
    print(split_word('ioxxoj[asdfgh]zxcvbnioxxoj[asdfgh]zxcvbn'))

test_split_word()

def has_abba(word):
    while len(word) >= 4:
        to_test = word[:4]
        if to_test[0] == to_test[3] and to_test[1] == to_test[2] and to_test[0] != to_test[1]:
            return True
        word = word[1:]
    return False

def test_has_abba():
    assert has_abba('ABBA') == True
    assert has_abba('aBBa') == True
    assert has_abba('oxxo') == True
    assert has_abba('ioxxoj') == True
    assert has_abba('aaaa') == False
    assert has_abba('zxcvbn') == False

def support_tls(word):
    outside, inside = split_word(word)
    if any(map(has_abba, inside)):
        return False
    elif any(map(has_abba, outside)):
        return True
    else:
        return False

def test_support_tls():
    assert support_tls('abba[mnop]qrst') == True
    assert support_tls('abcd[bddb]xyyx') == False
    assert support_tls('aaaa[qwer]tyui') == False
    assert support_tls('ioxxoj[asdfgh]zxcvbn') == True

test_has_abba()
test_support_tls()

print(len([d for d in data if support_tls(d)]))
