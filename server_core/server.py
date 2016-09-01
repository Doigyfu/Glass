#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import print_function

import codecs

players = {}


def u(x):
    return codecs.unicode_escape_decode(x)[0]


from random import randint
from sys import exit as sysex

from quarry.net.server import ServerFactory, ServerProtocol

import packet as packet
import randomdata


class Mineserver(ServerProtocol):
    def packet_login_start(self, buff):
        if not options.down:
            ServerProtocol.packet_login_start(self, buff)
        else:
            buff.discard()
            self.close(options.downmsg)

    def player_joined(self):
        ServerProtocol.player_joined(self)
        self.ip = self.remote_addr.host
        self.entity_id = randomdata.getFreeId()
        self.fquid = self.username + "[/" + self.ip + "](" + str(self.uuid) + ")"
        # self.base_scba_split = list("PyMINESERVER")
        # self.anim_i = 0
        players[self.entity_id] = self
        self.logger.info("UUID of player {0} is {1}".format(self.username, self.uuid))
        self.game(self.entity_id, 1, 0, 1, options.maxplayers, "default", False)

        self.spawn_pos(0, 66, 0)

        self.abilities(True, True, True, True, 0.2, 0.2)
        self.pos_look(0, 66, 0, 0, 0, False)
        self.rain(True)
        self.empty_chunk(0, 0)
        # packet.block_change(self, 0, 64, 0, 1)

        # if self.protocol_version == 47: packet.plist_head_foot(self, u"§6P§2yMINESERVER§r", u"§eEnjoy the Test§r# ")
        # if self.protocol_version == 47: self.tasks.add_loop(1.0 / 20, self.anim_frame_scb)
        self.logger.info("{0} ({1}) logged in with entity id {2}".format(self.username, self.ip,
                                                                         self.entity_id) + " at ((0.0, 64.0, 0.0))")
        # Schedule 6-second sending of keep-alive packets.
        self.tasks.add_loop(6, self.keepalive_send)
        # self.eobj_byid = eobj_byid
        # pushChat(self, "\u00A7e" + self.username + " has joined the game\u00A7r", 1)

        # Send welcome title and subtitle
        self.title(options.wtitle)
        self.subtitle(options.wst)

        self.chat_json(randomdata.join_json(self), 1)

    def player_left(self):
        ServerProtocol.player_left(self)
        del players[self.entity_id]
        # pushChatCall(self, "\u00A7e" + self.username + " has left the game\u00A7r", 1, self.destroy)

    def keepalive_send(self):
        self.last_keepalive = random_digits(randint(4, 9))
        packet.keep_alive(self, self.last_keepalive)

    def packet_keep_alive(self, buff):
        if buff.unpack_varint() == self.last_keepalive:
            pass
        else:
            if self.keepalive_miss < 4:
                self.keepalive_miss += 1
            else:
                buff.discard()
                self.logger.info(
                    "Kicking player " + self.username + " for not responding to keepalives for 24 seconds.")
                self.close("Timed out: did not ping for 24 seconds.")

    def global_chat(self, message):
        for entity_id, player_object in players.iteritems():
            self.chat(message)

    # import commands.cmds as cmds

    def handle_command(self, command_string):
        self.logger.info("Player " + self.username + " issued server command: " + command_string)
        command_list = command_string.split(" ")  # Command list - e.g ['/login','123123123','123123123']
        command, arguments = command_list[0], command_string.split(" ")[1:]  # Get command and arguments
        print(command, arguments)
        cmdobj = {
            "command": command,
            "args_raw": arguments,
            # "scope": self,
            "chat_raw": command_string
        }
        # if command not in cmds.baseList: cmds.InvalidCommand.cmd.begin(cmds.InvalidCommand.cmd(), cmdobj)
        # else: cmds.baseList[command].begin(cmds.baseList[command](), cmdobj)

    def packet_chat_message(self, buff):
        chat_message = buff.unpack_string()
        if chat_message[0] == '/':
            self.handle_command(chat_message)
        else:
            self.global_chat(chat_message)

    # print(handle_command("/login 123123123 123123123"))

    def destroy(self):
        players[self.entity_id] = None

    def anim_frame_scb(self):
        self.sstmp = self.base_scba_split
        if self.anim_i >= len(self.sstmp): self.anim_i = 0
        self.sstmp[self.anim_i] = u"§6" + self.sstmp[self.anim_i] + u"§2"
        packet.plist_head_foot(self, u"§2" + self.sstmp[self.anim_i] + u"§r", u"§eEnjoy the Test§r")
        self.anim_i += 1

    def empty_chunk(self, x, z):  # args: chunk position ints (x, z)
        self.send_packet("chunk_data", self.buff_type.pack('ii?H', x, z, True, 0) + self.buff_type.pack_varint(0))

    def rain(self, state):  # args: bool for rain
        if state:
            self.send_packet("change_game_state", self.buff_type.pack('Bf', 2, 0.0))
        else:
            self.send_packet("change_game_state", self.buff_type.pack('Bf', 1, 0.0))

    def pos_look(self, x, y, z, xr, yr, og):  # args: num (x, y, z, x rotation, y rotation, on-ground[bool])
        self.send_packet("player_position_and_look",
                         self.buff_type.pack('dddffb', float(x), float(y), float(z), float(xr), float(yr), og))

    def abilities(self, flying, fly, god, creative, fly_speed,
                  walk_speed):  # args: bool (if flying, if can fly, if no damage, if creative, (num) fly speed, walk speed)
        atmp1 = 0
        if flying: atmp1 = atmp1 | 0x02
        if fly: atmp1 = atmp1 | 0x04
        if god: atmp1 = atmp1 | 0x08
        if creative: atmp1 = atmp1 | 0x01
        self.send_packet("player_abilities", self.buff_type.pack('bff', atmp1, float(fly_speed), float(walk_speed)))

    def spawn_pos(self, x, y, z):  # args: (x, y, z) int
        self.send_packet("spawn_position",
                         self.buff_type.pack('q', ((x & 0x3FFFFFF) << 38) | ((y & 0xFFF) << 26) | (z & 0x3FFFFFF)))

    def game(self, entity_id, gamemode, dimension, difficulty, max_players, type,
             dbg):  # args: int (entity id, gamemode, dimension, difficulty, max players, level type[str], reduced f3 info[bool])
        self.send_packet("join_game", self.buff_type.pack('iBbBB', entity_id, gamemode, dimension, difficulty,
                                                          max_players) + self.buff_type.pack_string(
            type) + self.buff_type.pack('?', dbg))

    def chat(self, message_bytes, position=0):  # args: (message[str], tp[int])
        self.send_packet('chat_message',
                         self.buff_type.pack_chat(u(message_bytes)) + self.buff_type.pack('b',
                                                                                          position)) if not self == None else u(
            "")

    def chat_json(self, message_bytes, position=0):  # args: (message[dict], tp[int])
        self.send_packet('chat_message', self.buff_type.pack_json(message_bytes) + self.buff_type.pack('b', position))

    def title(self, msgb):
        self.send_packet('title', self.buff_type.pack_varint(0) + self.buff_type.pack_chat(msgb))

    def subtitle(self, msgb):
        self.send_packet('title', self.buff_type.pack_varint(1) + self.buff_type.pack_chat(msgb))

    def title_json(self, msgb):
        self.send_packet('title', self.buff_type.pack_varint(0) + self.buff_type.pack_json(msgb))

    def subtitle_json(self, msgb):
        self.send_packet('title', self.buff_type.pack_varint(1) + self.buff_type.pack_json(msgb))

    def keep_alive(self, vienc):  # args: (varint data[int])
        self.send_packet("keep_alive", self.buff_type.pack_varint(vienc))

    def kick(self, rson):  # args: (reason[str])
        self.close(rson)

    def plist_head_foot(self, msga, msgb):  # args: str (header, footer)
        self.send_packet("player_list_header_footer", self.buff_type.pack_chat(msga) + self.buff_type.pack_chat(msgb))

    def block_change(self, x, y, z, id):  # args: int (x, y, z, block id)
        self.send_packet("block_change", self.buff_type.pack('q', ((x & 0x3FFFFFF) << 38) | ((y & 0xFFF) << 26) | (
            z & 0x3FFFFFF)) + self.buff_type.pack_varint((id << 4) | 0))


class MineFactory(ServerFactory):
    protocol = Mineserver


def random_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def main(args):
    # Parse options
    import optparse
    parser = optparse.OptionParser(usage="usage: %prog [options]")
    parser.add_option("-a", "--host", dest="host", default="", help="address to listen on")
    parser.add_option("-p", "--port", dest="port", default="25565", type="int", help="port to listen on")
    parser.add_option("-m", "--motd", dest="motd", default="PyMineserver: Test. Hello! Now with joining! §b§l\\o/§r",
                      type="string", help="motd to send to clients")
    parser.add_option("-o", "--offline", action="store_false", dest="auth", default=True,
                      help="offline mode does not authenticate players!")
    parser.add_option("-k", "--downtime", action="store_true", dest="down", default=False,
                      help="kick players with downtimemsg")
    parser.add_option("-q", "--downtimemsg", dest="downmsg",
                      default="Sorry, but this server is currently down for maintenance. Check back soon!",
                      help="message to kick for downtime with")
    parser.add_option("-w", "--wtitle", dest="wtitle", default="Welcome to Mineserver!",
                      help="title to display on join")
    parser.add_option("-s", "--wsubtitle", dest="wst", default="Enjoy this test server!",
                      help="subtitle to display on join")
    parser.add_option("-l", "--max-players", dest="maxplayers", default=20, help="max player count/limit")
    parser.add_option("-f", "--favicon", dest="favicon", default="creeper.png",
                      help="relative path to server favicon in png")
    global options
    (options, args) = parser.parse_args(args)

    # Warn about auth mode
    if options.auth:
        print(
            "Mineserver (warn/INFO)> Mineserver is running in online mode. All players must be authenticated to join. *(ONLINE)*")
    else:
        print(
            "Mineserver (WARN/info)> Mineserver is running in offline mode. Players can join with fake UUIDs and names without authentication! *[OFFLINE]*!")

    # Create factory
    factory = MineFactory()
    factory.motd = options.motd
    factory.online_mode = options.auth
    factory.favicon = options.favicon

    # Listen
    factory.listen(options.host, options.port)
    factory.run()


if __name__ == "__main__":
    print("Mineserver (warn/CRIT)> You should NOT be invoking this directly! Use mineserver.py.")
    sysex(1)
