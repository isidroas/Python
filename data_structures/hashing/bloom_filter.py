from hashlib import sha1

LOG_ADD = """\
[exists] old =    {}
         added =  {}
         new =    {}
"""


class Bloom:
    def __init__(self, size=8):
        self.bitstring = 0b00000000
        self.size = size
        self.mask = 2**size - 1

    def add(self, value):
        old = self.bitstring
        new = self.hash(value)
        self.bitstring |= new
        print(
            f"""\
[add] value = {value}
      old =   {self.format_bin(old)}
      added = {self.format_bin(new)}
      new =   {self.format_bin(self.bitstring)}
"""
        )

    def exists(self, value):
        h = self.hash(value)
        and_bitwise = h & self.bitstring
        # warning: h could be zero
        res = and_bitwise == h

        print(
            f"""\
[exists] value =    {value}
         ask =      {self.format_bin(h)}
         bistring = {self.format_bin(self.bitstring)}
         and =      {self.format_bin(and_bitwise)}
         res =      {res}
"""
        )
        return res

    def format_bin(self, value):
        res = bin(value)[2:]
        return res.zfill(self.size)

    def hash(self, value):
        b = sha1(value.encode()).digest()
        new = int.from_bytes(b, 'big')
        #new = b[0]
        # strip bytes
        new &= self.mask
        return new


def test():
    b = Bloom()
    b.add("titanic")
    b.add("avatar")

    assert b.exists("titanic")
    assert b.exists("avatar")

    assert not b.exists("parasite")
    assert b.exists("pulp fiction")
