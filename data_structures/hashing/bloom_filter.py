from hashlib import sha256, md5
from random import randint, choices
import string


class Bloom:
    def __init__(self, size=8):
        self.bitstring = 0b00000000
        self.size = size

    def add(self, value):
        new = self.hash(value)
        self.bitstring |= new
        print(
            f"""\
[add] value =       {value}
      added =       {self.format_bin(new)}
      bitstring =   {self.format_bin(self.bitstring)}
"""
        )

    def exists(self, value):
        h = self.hash(value)
        res = (h & self.bitstring) == h

        print(
            f"""\
[exists] value =    {value}
         ask =      {self.format_bin(h)}
         bistring = {self.format_bin(self.bitstring)}
         res =      {res}
"""
        )
        return res

    def format_bin(self, value):
        res = bin(value)[2:]
        return res.zfill(self.size)

    def hash(self, value):
        res = 0b0
        for func in (sha256, md5):
            b = func(value.encode()).digest()
            position = int.from_bytes(b, 'little') % self.size
            res |= 2 **position
        return res


def test():
    b = Bloom()
    b.add("titanic")
    b.add("avatar")

    assert b.exists("titanic")
    assert b.exists("avatar")

    assert not b.exists("the goodfather")
    assert not b.exists("interstellar")
    assert not b.exists("Parasite")
    assert not b.exists("Pulp fiction")


def random_string(size):
    return ''.join(choices(string.ascii_lowercase + ' ', k=size))

#def test_prob():
#    SIZE = 64
#    added = {random_string(100) for i in range(20)}
#    not_added = {random_string(100) for i in range(1000)}
#    b = Bloom(size = SIZE)
#    for a in added:
#        b.add(a)
#    fails = 0
#    for n in not_added:
#        if b.exists(n):
#            fails+=1
#    print(f'total = {len(not_added)}, fails = {fails}, prob = {fails/len(not_added)}')
#    n_possible = SIZE
#    n_ones = bin(b.bitstring).count('1')
#    print(f'expected_probability = {n_ones/n_possible}')
#    assert False
