'''class ExtendedBuffer(Buffer):
    @classmethod
    def pack_entity_metadata(cls, index, value_of_type_field, type_of_value):
        out = b""
        cls.pack("Bb")
'''


class Position(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def get_pos(self):
        return ((self.x & 0x3FFFFFF) << 38) | ((self.y & 0xFFF) << 26) | (self.z & 0x3FFFFFF)

    def get_xyz(self):
        return self.x, self.y, self.z

