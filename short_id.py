import time
from threading import Lock
from random import randrange

CHARACTERS = ('0123456789'
              'abcdefghijklmnopqrstuvwxyz'
              'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
_MAPPING = {char: i for i, char in enumerate(CHARACTERS)}


def encode(num_10):
    '''convert decimal number to other numeral'''
    acc = ''
    base_num = len(CHARACTERS)

    while num_10 > 0:
        num_10, mod = divmod(num_10, base_num)
        acc = CHARACTERS[mod] + acc
    return acc


def decode(num_x):
    '''recover other number to decimal number'''
    num_10 = 0
    base_num = len(CHARACTERS)

    for i, n in enumerate(reversed(num_x)):
        num_10 += _MAPPING[n] * base_num ** i
    return num_10


class ShortID:
    def __init__(self, characters=CHARACTERS):
        self.characters = characters
        self.base_num = len(characters)
        self.mapping = {char: i for i, char in enumerate(self.characters)}

        self._acc_base = randrange(0x400, 0x2000)
        self._acc_lock = Lock()

    def __iter__(self):
        return self

    def __next__(self):
        '''produces id with a very low probability of collision'''
        if self._acc_base < 0x1ffff:
            with self._acc_lock:
                self._acc_base += 1
        else:
            self._acc_base = randrange(0x400, 0x2000)  # reset

        mask = self._acc_base << (41 - self._acc_base.bit_length())
        normal_id = int(time.time() * 1000) ^ mask
        return self.encode(normal_id)

    def encode(self, normal_id):
        '''convert decimal number to other numeral'''
        short_id = ''

        while normal_id > 0:
            normal_id, mod = divmod(normal_id, self.base_num)
            short_id = self.characters[mod] + short_id

        return short_id

    def decode(self, short_id):
        '''recover other number to decimal number'''
        normal_id = 0

        for i, n in enumerate(reversed(short_id)):
            normal_id += self.mapping[n] * self.base_num ** i

        return normal_id

    def is_valid(self, short_id):
        '''check if a converted number is valid'''
        char_set = set(short_id)
        return char_set.issubset(self.characters)


id_generator = ShortID()
