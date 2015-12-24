# -*- coding: utf-8 -*-
from __future__ import print_function
from commands.cmds.BaseCommand import *
from packet.send import chat, kick
from server_core.chat import pushChat
from twisted.internet import reactor
from time import sleep

class cmd(BaseCommand):
    def process(self):
        #self.reason = " (" + "".join(self.cmdobj['args_raw'][-1:]) + ")"
        #self.osc = self.cmdobj['scope']
        #chat(self.osc, "\u00A7o\u00A78[" + self.osc.username + ": Stopping the server" + self.reason + "]\u00A7r", 1)
        #for plindex in self.osc.eobj_byid:
        #    kick(self.osc.eobj_byid[plindex], "\u00A7cThe server was shut down" + self.reason + ".\u00A7r")
        #sleep(1)
        print("Mineserver (INFO/warn)> The server is shutting down from /stop command signal.")
        reactor.removeAll()
        reactor.iterate()
        reactor.stop()