import permissions as perms
import randomdata as dats
import codecs

# here, type 'num' means float or int - the code converts to float.
def u(x):
    return codecs.unicode_escape_decode(x)[0]

def empty_chunk(self, x, z): # args: chunk position ints (x, z)
    self.send_packet("chunk_data", self.buff_type.pack('ii?H', x, z, True, 0) + self.buff_type.pack_varint(0))

def rain(self, state): # args: bool for rain
    if state: self.send_packet("change_game_state", self.buff_type.pack('Bf', 2, 0.0))
    else: self.send_packet("change_game_state", self.buff_type.pack('Bf', 1, 0.0))

def pos_look(self, x, y, z, xr, yr, og): # args: num (x, y, z, x rotation, y rotation, on-ground[bool])
    self.send_packet("player_position_and_look", self.buff_type.pack('dddffb', float(x), float(y), float(z), float(xr), float(yr), og))

def abilities(self, flying, fly, god, creative, fs, ws): # args: bool (if flying, if can fly, if no damage, if creative, (num) fly speed, walk speed)
    atmp1 = 0
    if flying: atmp1 = atmp1 | 0x02
    if fly: atmp1 = atmp1 | 0x04
    if god: atmp1 = atmp1 | 0x08
    if creative: atmp1 = atmp1 | 0x01
    self.send_packet("player_abilities", self.buff_type.pack('bff', atmp1, float(fs), float(ws)))

def spawn_pos(self, x, y, z): # args: (x, y, z) int
    self.send_packet("spawn_position", self.buff_type.pack('q', ((x & 0x3FFFFFF) << 38) | ((y & 0xFFF) << 26) | (z & 0x3FFFFFF)))

def game(self, eid, gm, dim, dfc, maxp, type, dbg): # args: int (entity id, gamemode, dimension, difficulty, max players, level type[str], reduced f3 info[bool])
    self.send_packet("join_game", self.buff_type.pack('iBbBB', eid, gm, dim, dfc, maxp) + self.buff_type.pack_string(type) + self.buff_type.pack('?', dbg))

def chat(self, msgb, tp): # args: (message[str], tp[int])
    self.send_packet('chat_message', self.buff_type.pack_chat(u(msgb)) + self.buff_type.pack('b', tp))

def chat_json(self, msgb, tp): # args: (message[dict], tp[int])
    self.send_packet('chat_message', self.buff_type.pack_json(msgb) + self.buff_type.pack('b', tp))