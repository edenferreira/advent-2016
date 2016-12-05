from hashlib import md5
from itertools import count

def hashes(door_id):
    for i in count(0):
        yield md5((door_id + str(i)).encode('utf-8')).hexdigest()


h = hashes(sys.argv[1])
password = [None] * 8

while None in password:
    current = ''
    while current[:5] != '00000':
        current = next(h)
    position = None
    try:
      position = int(current[5])
    except ValueError:
      continue

    value = current[6]
    if 0 <= position < 8:
      if password[position] is None:
        password[position] = value

print(''.join(password))

