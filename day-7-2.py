from itertools import chain

def flatten(it):
    return chain.from_iterable(it)

def uniq(ls):
    return list(set(ls))

data = [
    'aba[bab]xyz',
    'xyx[xyx]xyx',
    'aaa[kek]eke',
    'zazbz[bzb]cdb'
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

def is_aba(word):
    return word[0] == word[2] and word[0] != word[1]

def to_bab(word):
    assert is_aba(word)
    return word[1] + word[0] + word[1]

assert to_bab('aba') == 'bab'

def extract_abas(word):
    abas = []
    while len(word) > 2:
        to_test = word[:3]
        if is_aba(to_test):
            abas.append(to_test)
        word = word[1:]
    return abas

def has_aba(word):
    while len(word) >= 3:
        to_test = word[:3]
        if to_test[0] == to_test[2] and to_test[0] != to_test[1]:
            return True
        word = word[1:]
    return False


def test_has_aba():
    assert has_aba('ABA') == True
    assert has_aba('aBa') == True
    assert has_aba('oxo') == True
    assert has_aba('ioxoj') == True
    assert has_aba('aaa') == False
    assert has_aba('zxcvbn') == False

def support_tls(word):
    outside, inside = split_word(word)
    outside_abas = uniq(flatten(extract_abas(w) for w in outside))
    if not outside_abas:
        return False
    possible_babs = [to_bab(w) for w in outside_abas]
    for bab in possible_babs:
        for words in inside:
            if bab in words:
                return True
    return False

def test_support_tls():
    assert support_tls('aba[bab]xyz') == True
    assert support_tls('xyx[xyx]xyx') == False
    assert support_tls('aaa[kek]eke') == True
    assert support_tls('zazbz[bzb]cdb') == True

test_support_tls()

print(len([d for d in data if support_tls(d)]))

