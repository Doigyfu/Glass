from quarry.utils.buffer import Buffer


# Will provide buffer for sendind complicated stuff, like Entity Metadata
class ExtendedBuffer(Buffer):
    @classmethod
    def pack_slot_data(cls, block_id, item_count=1, item_damage=1, nbt_data=None):
        return cls.pack("h", -1)

    @classmethod
    @classmethod
    def pack_entity_metadata(cls, index=1, type=1, value=1):
        bitmask = 0
        bitmask = 0 | 0x01  # On fire
        buff = cls.pack("b", bitmask)
        buff += cls.pack_varint()


class Position(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def get_pos(self):
        return ((self.x & 0x3FFFFFF) << 38) | ((self.y & 0xFFF) << 26) | (self.z & 0x3FFFFFF)

    def get_xyz(self):
        return self.x, self.y, self.z

