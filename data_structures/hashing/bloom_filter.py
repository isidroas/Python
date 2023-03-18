from hashlib import sha1


class Bloom:
    def __init__(self, size=8):
        self.bitstring = 0b00000000
        self.size = size
        self.mask = 2**size - 1

    def add(self, value):
        new = self.hash(value)
        self.bitstring |= new

    def exists(self, value):
        h = self.hash(value)
        print(
            "[exists]\th = \t\t{}\n\t\tbistring = \t{}\n".format(
                self.format_bin(h), self.format_bin(self.bitstring)
            )
        )
        # warning: h could be zero
        return (h & self.bitstring) == h

    def format_bin(self, value):
        res = bin(value)[2:]
        return res.zfill(self.size)

    def hash(self, value):
        b =sha1(value.encode()).digest()
        #new = int.from_bytes(b)
        new = b[0]
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
    assert not b.exists("pulp fiction")
