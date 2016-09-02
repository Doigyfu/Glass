#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import print_function

import codecs


def u(x):
    return codecs.unicode_escape_decode(x)[0]


players = {}
import random

from quarry.net.server import ServerFactory, ServerProtocol
import randomdata
from types import Position

id_counter = 0

class Mineserver(ServerProtocol):
    def packet_login_start(self, buff):
        ServerProtocol.packet_login_start(self, buff)

    def get_free_id(self):
        global id_counter
        id_counter += 1
        return id_counter

    def player_joined(self):
        ServerProtocol.player_joined(self)
        self.ip = self.remote_addr.host
        self.spawn_position = Position(0, 66, 0)
        self.entity_id = self.get_free_id()
        # self.send_chat(str(self.entity_id))
        self.default_gamemode = 1  # 0: Survival, 1: Creative, 2: Adventure, 3: Spectator. Bit 3 (0x8) is the hardcore flag.
        self.dimension = 0  # -1: Nether, 0:Overworld, 1:End
        self.difficulty = 0  # 0:peaceful,1:easy,2:normal,3:hard
        self.max_players = 25  # Was once used by the client to draw the player list, but now is ignored
        self.level_type = "default"  # default, flat, largeBiomes, amplified, default_1_1
        self.reduced_debug_info = False  # If true, a Notchian client shows reduced information on the debug screen.
        #self.send_chat(str(self.uuid))
        players[self.entity_id] = self
        self.logger.info("UUID of player {0} is {1}".format(self.username, self.uuid))
        self.send_game(self.entity_id, self.default_gamemode, self.dimension, self.difficulty, self.max_players,
                       "default",
                       False)
        self.send_spawn_pos(self.spawn_position)
        self.send_abilities(True, True, True, True, 0.2, 0.2)
        self.send_position_and_look(self.spawn_position, 0, 0, False)
        self.send_empty_chunk(0, 0)
        self.logger.info("{0} ({1}) logged in with entity id {2}".format(self.username, self.ip,
                                                                         self.entity_id) + " at ((0.0, 64.0, 0.0))")
        # Schedule 6-second sending of keep-alive packets.
        self.tasks.add_loop(6, self.keepalive_send)
        self.send_chat_json(randomdata.join_json(self), 1)
        try:
            self.player_join_event()
        except Exception as ex:
            print(ex.message)
            print("ERROR IN JOIN EVENT!")

    def player_left(self):
        try:
            self.player_leave_event()
        except Exception as ex:
            print(ex.message)
            print("ERROR IN LEAVE EVENT!")
        del players[self.entity_id]
        ServerProtocol.player_left(self)

    def keepalive_send(self):
        self.last_keepalive = random.randint(6969696, 96969696)  # Some magic numbers here :)
        self.send_keep_alive(self.last_keepalive)

    def packet_keep_alive(self, buff):
        if buff.unpack_varint() == self.last_keepalive:
            pass
        else:
            if self.keepalive_miss < 4:  # Check for keepalive count
                self.keepalive_miss += 1  # Increment by 1
            else:  # If keepalive miss more than 4, the player probably lagged out, so let's kick him!
                buff.discard()
                self.logger.info(
                    "Kicking player " + self.username + " for not responding to keepalives for 24 seconds.")
                self.close("Timed out: did not ping for 24 seconds.")

    def handle_chat(self, message):
        message = message.encode('utf8')
        # TODO: add chat event to plugins
        self.send_chat("{0}: {1}".format(self.username, message))

    def handle_command(self, command_string):

        # TODO: add command event to plugins
        self.logger.info("Player " + self.username + " issued server command: " + command_string)
        command_list = command_string.split(" ")  # Command list - e.g ['/login','123123123','123123123']
        command, arguments = command_list[0], command_string.split(" ")[1:]  # Get command and arguments
        # TODO: Implement this as plugin
        if command == "stop":
            from twisted.internet import reactor
            reactor.removeAll()
            reactor.iterate()
            reactor.stop()
        self.logger.info(command + str(arguments))

    def packet_player_position(self, buff):
        x, y, z, on_ground = buff.unpack('ddd?')
        # for entity_id,player in players.iteritems():
        #player.send_spawn_player(entity_id,player.uuid,x,y,z,0,0)

    def packet_chat_message(self, buff):
        chat_message = buff.unpack_string()
        if chat_message[0] == '/':
            self.handle_command(chat_message[1:])  # Slice to shrink slash
        else:
            self.handle_chat(chat_message)

    #def send_spawn_player(self,entity_id,player_uuid,x,y,z,yaw,pitch):


    def send_empty_chunk(self, x, z):  # args: chunk position ints (x, z)
        self.send_packet("chunk_data", self.buff_type.pack('ii?H', x, z, True, 0) + self.buff_type.pack_varint(0))

    def send_change_game_state(self, reason, state):  # http://wiki.vg/Protocol#Change_Game_State
        self.send_packet("change_game_state", self.buff_type.pack('Bf', reason, state))

    def send_position_and_look(self, position, xr, yr,
                               on_ground):  # args: num (x, y, z, x rotation, y rotation, on-ground[bool])
        x, y, z = position.get_xyz()
        self.send_packet("player_position_and_look",
                         self.buff_type.pack('dddffb', float(x), float(y), float(z), float(xr), float(yr), on_ground))

    def send_abilities(self, flying, fly, god, creative, fly_speed,
                       walk_speed):  # args: bool (if flying, if can fly, if no damage, if creative, (num) fly speed, walk speed)
        bitmask = 0
        if flying: bitmask = bitmask | 0x02
        if fly: bitmask = bitmask | 0x04
        if god: bitmask = bitmask | 0x08
        if creative: bitmask = bitmask | 0x01
        self.send_packet("player_abilities", self.buff_type.pack('bff', bitmask, float(fly_speed), float(walk_speed)))

    def send_spawn_pos(self, position):  # args: (x, y, z) int
        self.send_packet("spawn_position",
                         self.buff_type.pack('q', position.get_pos())  # get_pos() is long long type
                         )

    def send_game(self, entity_id, gamemode, dimension, difficulty, max_players, type,
                  dbg):  # args: int (entity id, gamemode, dimension, difficulty, max players, level type[str], reduced f3 info[bool])
        self.send_packet("join_game",
                         self.buff_type.pack('iBbBB',
                                             entity_id, gamemode, dimension, difficulty,
                                             max_players) + self.buff_type.pack_string(type) +
                         self.buff_type.pack('?', dbg)
                         )

    def send_chat(self, message_bytes, position=0):  # args: (message[str], position[int])
        for entid, player in players.iteritems():
            player.send_packet('chat_message',

                               )

    def send_chat_json(self, message_bytes, position=0):  # args: (message[dict], tp[int])
        self.send_packet('chat_message', self.buff_type.pack_json(message_bytes) + self.buff_type.pack('b', position))

    def send_title(self, message, json=False, position=0):  # message, json msg, position: 0 for title, 1 for subtitle
        if json:
            self.send_packet('title', self.buff_type.pack_varint(position) + self.buff_type.pack_json(message))
        else:
            self.send_packet('title', self.buff_type.pack_varint(position) + self.buff_type.pack_chat(message))

    def send_keep_alive(self, keepalive_id):  # args: (varint data[int])
        self.send_packet("keep_alive", self.buff_type.pack_varint(keepalive_id))

    def send_kick(self, reason):  # args: (reason[str])
        self.close(reason)  # Close connection

    def send_plist_head_foot(self, header, footer):  # args: str (header, footer)
        self.send_packet("player_list_header_footer",
                         self.buff_type.pack_chat(header) +
                         self.buff_type.pack_chat(footer))

    def send_block_change(self, x, y, z, block_id):  # args: int (x, y, z, block id)
        self.send_packet("block_change", self.buff_type.pack('q', ((x & 0x3FFFFFF) << 38) | ((y & 0xFFF) << 26) | (
            z & 0x3FFFFFF)) + self.buff_type.pack_varint((block_id << 4) | 0))


class MineFactory(ServerFactory):
    #log_level = logging.DEBUG  # For testing
    protocol = Mineserver
