# -*- coding: utf-8 -*-
from __future__ import print_function
from commands.cmds.BaseCommand import *
from packet.send import chat, kick
from server_core.chat import pushChat
from sys import exit as sysex

class cmd(BaseCommand):
    def process(self):
        global eobj_byid
        try:
            self.reason = " (" + self.cmdobj['args_raw'][0] + ")"
        except IndexError:
            self.reason = ""
        chat(self.cmdobj['scope'], "\u00A7o\u00A78[" + self.cmdobj['scope'].username + ": Stopping the server" + self.reason + "]\u00A7r", 1)
        self.dokickprocess()
        for plindex in eobj_byid:
            leftcounter = leftcounter + 1
        if leftcounter != 0:
            self.dokickprocess()
        else:
            print("Mineserver (INFO/warn)> The server is shutting down from /stop command signal. Reason:" + self.reason)
            sysex()
    def dokickprocess(self):
        global eobj_byid
        for plindex in eobj_byid:
            kick(eobj_byid[plindex], "\u00A7cThe server was shut down" + self.reason + ".\u00A7r")