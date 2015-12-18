#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from quarry.net.server import ServerFactory, ServerProtocol
from random import randint
from os import system
import packet as p
import permissions as perms
import randomdata as dats
import commands as cmd

idcounter = -1
eobj_byid = {}

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
        self.eid = getFreeId()
        self.fquid = self.username + "[/" + self.ip + "](" + str(self.uuid) + ")"
        eobj_byid[self.eid] = self
        self.logger.info("%s successfully logged in." % self.fquid)

        p.game(self, self.eid, 1, 0, 1, options.maxplayers, "default", False)
        p.spawn_pos(self, 0, 64, 0)
        p.abilities(self, True, True, True, True, 0.2, 0.2)
        p.pos_look(self, 0, 64, 0, 0, 0, False)
        p.rain(self, True)
        p.empty_chunk(self, 0, 0)
        
        # Schedule 6-second sending of keep-alive packets.
        self.tasks.add_loop(6, self.keepalive_send)
        
        pushChat("\u00A7e" + self.username + " has joined the game\u00A7r", 1)
        
        # Send welcome title and subtitle
        p.title(self, options.wtitle)
        p.subtitle(self, options.wst)
        
        p.chat_json(self, dats.join_json(self), 1)
    def player_left(self):
        ServerProtocol.player_left(self)
        pushChat("\u00A7e" + self.username + " has left the game\u00A7r", 1)
        eobj_byid[self.eid] = None
    def keepalive_send(self):
        self.last_keepalive = random_digits(randint(4, 9))
        p.keep_alive(self, self.last_keepalive)
    def packet_keep_alive(self, buff):
        if buff.unpack_varint() == self.last_keepalive: pass
        else:
            if self.keepalive_miss < 4:
                self.keepalive_miss += 1
            else:
                buff.discard()
                self.logger.info("Kicking player " + self.username + " for not responding to keepalives for 24 seconds.")
                self.close("Timed out: did not ping for 24 seconds.")
    def packet_chat_message(self, buff):
        _atmp = buff.unpack_string()
        cmd.handle(self, _atmp) if _atmp[0] == "/" else pushChat("<" + self.username + "> " + _atmp.replace("\u00A7", ""), 0)

class MineFactory(ServerFactory):
    protocol = Mineserver


def getFreeId():
    global idcounter
    idcounter += 1
    return idcounter


def random_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def pushChat(msga, t):
    for pobja in eobj_byid:
        p.chat(eobj_byid[pobja], msga, t)


def main(args):
    # Parse options
    import optparse
    parser = optparse.OptionParser(usage="usage: %prog [options]")
    parser.add_option("-a", "--host", dest="host", default="", help="address to listen on")
    parser.add_option("-p", "--port", dest="port", default="25565", type="int", help="port to listen on")
    parser.add_option("-m", "--motd", dest="motd", default="PyMineserver: Test. Hello! Now with joining! §b§l\\o/§r", type="string", help="motd to send to clients")
    parser.add_option("-o", "--offline", action="store_false", dest="auth", default=True, help="offline mode does not authenticate players!")
    parser.add_option("-k", "--downtime", action="store_true", dest="down", default=False, help="kick players with downtimemsg")
    parser.add_option("-q", "--downtimemsg", dest="downmsg", default="Sorry, but this server is currently down for maintainence. Check back soon!", help="message to kick for downtime with")
    parser.add_option("-w", "--wtitle", dest="wtitle", default="Welcome to Mineserver!", help="title to display on join")
    parser.add_option("-s", "--wsubtitle", dest="wst", default="Enjoy this test server!", help="subtitle to display on join")
    parser.add_option("-l", "--max-players", dest="maxplayers", default=20, help="max player count/limit")
    parser.add_option("-f", "--favicon", dest="favicon", default="creeper.png", help="relative path to server favicon in png")
    global options
    (options, args) = parser.parse_args(args)
    
    # Warn about auth mode
    if options.auth:
        print("Mineserver (warn/INFO)> Mineserver is running in online mode. All players must be authenticated to join. *(ONLINE)*")
    else:
        print("Mineserver (WARN/info)> Mineserver is running in offline mode. Players can join with fake UUIDs and names without authentication! *[OFFLINE]*!")

    # Create factory
    factory = MineFactory()
    factory.motd = options.motd
    factory.online_mode = options.auth
    factory.favicon = options.favicon

    # Listen
    factory.listen(options.host, options.port)
    factory.run()


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])