#!/usr/bin/env python
# -*- coding: utf-8 -*-

###BUILD-IN STUFF
from __future__ import print_function

import random

players = {}

###PROTOCOL AND SERVER STUFF
from quarry.net.server import ServerFactory, ServerProtocol
import serverdata
from serverdata.values import Position

id_counter = 0  # We need to have unique ID for all entities in a server

__all__ = ["MineFactory", "Mineserver"]


class Mineserver(ServerProtocol):
    def packet_login_start(self, buff):
        ServerProtocol.packet_login_start(self, buff)

    def get_free_id(self):  # Get free ID for entity_id
        global id_counter  # Because TWISTED isn't threaded, we can safely call a global variable
        id_counter += 1
        return id_counter

    # Plugin event method
    def plugin_event(self, event_name, *args, **kwargs):
        self.factory.plugin_system.call_event(event_name, self, *args, **kwargs)

    def player_joined(self):
        ServerProtocol.player_joined(self)
        self.ip = self.remote_addr.host
        self.position = Position(0, 66, 0)
        self.entity_id = self.get_free_id()
        self.default_gamemode = 1  # 0: Survival, 1: Creative, 2: Adventure, 3: Spectator. Bit 3 (0x8) is the hardcore flag.
        self.dimension = 0  # -1: Nether, 0:Overworld, 1:End
        self.difficulty = 0  # 0:peaceful,1:easy,2:normal,3:hard
        self.level_type = "default"  # default, flat, largeBiomes, amplified, default_1_1
        self.reduced_debug_info = False  # If true, a Notchian client shows reduced information on the debug screen.
        players[
            self.entity_id] = self  # add player object to dict eid:player , so we can iterate over ALL players on the server
        self.logger.info("UUID of player {0} is {1}".format(self.username, self.uuid))
        self.nickname = self.username
        self.send_game(self.entity_id, self.default_gamemode, self.dimension, self.difficulty, "default", False)
        self.send_spawn_pos(self.position)
        self.send_abilities(True, True, True, True, 0.2, 0.2)
        self.send_position_and_look(self.position, 0, 0, False)
        self.send_empty_chunk(0, 0)
        self.logger.info("{0} ({1}) logged in with entity id {2}".format(self.username, self.ip,
                                                                         self.entity_id) + " at ((0.0, 64.0, 0.0))")
        # Schedule 6-second sending of keep-alive packets.
        self.tasks.add_loop(1, self.keepalive_send)
        self.send_chat_json(serverdata.join_json(self), 1)  # Print welcome message
        self.plugin_event("player_join")

    def player_left(self):
        self.plugin_event("player_leave")
        del players[self.entity_id]
        ServerProtocol.player_left(self)

    def keepalive_send(self):
        self.last_keepalive = random.randint(6969696, 96969696)  # Some magic numbers here :)
        self.send_keep_alive(self.last_keepalive)

    def packet_keep_alive(self, buff):
        if buff.unpack_varint() == self.last_keepalive:
            pass
        else:
            if self.keepalive_miss < 2:  # Check for keepalive count
                self.keepalive_miss += 1  # Increment by 1
            else:  # If keepalive miss more than 4, the player probably lagged out, so let's kick him!
                buff.discard()
                self.logger.info(
                    "Kicking player " + self.username + " for not responding to keepalives for 24 seconds.")
                self.close("Timed out: did not ping for 24 seconds.")

    def handle_chat(self, message):
        message = message.encode('utf8')
        self.plugin_event("player_chat", message)
        message = "<{0}> {1}".format(self.username, message)
        self.logger.info(message)  # Write chat message in server console
        self.send_chat(message)  # send chat message to all players on server

    def handle_command(self, command_string):
        self.logger.info("Player " + self.username + " issued server command: " + command_string)
        command_list = command_string.split(" ")  # Command list - e.g ['/login','123123123','123123123']
        command, arguments = command_list[0], command_string.split(" ")[1:]  # Get command and arguments
        self.plugin_event("player_command", command, arguments)

    def packet_player_position(self, buff):
        x, y, z, on_ground = buff.unpack('ddd?')  # X Y Z - coordinates, on ground - boolean
        self.plugin_event("player_move", x, y, z, on_ground)
        self.position.set(x, y, z)
        # Currently don't work
        '''for eid,player in players.iteritems():
            if player!=self:
                player.send_spawn_player(eid,player.uuid,x,y,z,0,0)
        '''

    def packet_chat_message(self, buff):
        chat_message = buff.unpack_string()
        if chat_message[0] == '/':
            self.handle_command(chat_message[1:])  # Slice to shrink slash
        else:
            self.handle_chat(chat_message)

    '''def send_spawn_player(self,entity_id,player_uuid,x,y,z,yaw,pitch):
        buff = self.buff_type.pack_varint(entity_id)+self.buff_type.pack_uuid(player_uuid)+self.buff_type.pack("dddbbBdb",x,y,z,yaw,pitch,0,7,health)
        self.send_packet("spawn_player",buff)
    '''

    def send_empty_chunk(self, x, z):  # args: chunk position ints (x, z)
        self.send_packet("chunk_data", self.buff_type.pack('ii?H', x, z, True, 0) + self.buff_type.pack_varint(0))

    def send_change_game_state(self, reason, state):  # http://wiki.vg/Protocol#Change_Game_State
        self.send_packet("change_game_state", self.buff_type.pack('Bf', reason, state))

    def set_position(self, x, y, z, xr=0, yr=0, on_ground=False):
        self.position.set(x, y, z)
        self.send_position_and_look(self.position, xr, yr, on_ground)

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

    def send_game(self, entity_id, gamemode, dimension, difficulty, level_type,
                  dbg):  # args: int (entity id, gamemode, dimension, difficulty, max players, level type[str], reduced debug info[bool])
        max_players = 25  # This is no longer used in Minecraft protocol
        self.send_packet("join_game",
                         self.buff_type.pack('iBbBB',
                                             entity_id, gamemode, dimension, difficulty,
                                             max_players) + self.buff_type.pack_string(level_type) +
                         self.buff_type.pack('?', dbg)
                         )

    def send_chat_all(self, message_bytes, position=0):  # Send chat message for all players
        for player in players.values():
            player.send_packet('chat_message',
                               player.buff_type.pack_chat(message_bytes) +
                               player.buff_type.pack('b', position)
                               )

    def send_chat(self, message_bytes, position=0):  # args: (message[str], position[int])
        self.send_packet('chat_message',
                         self.buff_type.pack_chat(message_bytes) +
                         self.buff_type.pack('b', position)
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

    def send_plist_head_foot(self, header, footer):  # args: str (header, footer)
        self.send_packet("player_list_header_footer",
                         self.buff_type.pack_chat(header) +
                         self.buff_type.pack_chat(footer))

    def send_block_change(self, x, y, z, block_id):  # args: int (x, y, z, block id)
        self.send_packet("block_change", self.buff_type.pack('q', ((x & 0x3FFFFFF) << 38) | ((y & 0xFFF) << 26) | (
            z & 0x3FFFFFF)) + self.buff_type.pack_varint((block_id << 4) | 0))


class MineFactory(ServerFactory):
    protocol = Mineserver
