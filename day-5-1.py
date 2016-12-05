from hashlib import md5
from itertools import count

def hashes(door_id):
    for i in count(0):
        yield md5((door_id + str(i)).encode('utf-8')).hexdigest()


h = hashes(sys.argv[1])
password = ''

while len(password) < 8:
    current = ''
    while current[:5] != '00000':
        current = next(h)
    password += current[6]

print(password)
