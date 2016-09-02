class Position():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def get_pos(self):
        return ((self.x & 0x3FFFFFF) << 38) | ((self.y & 0xFFF) << 26) | (self.z & 0x3FFFFFF)

    def get_xyz(self):
        return self.x, self.y, self.z
