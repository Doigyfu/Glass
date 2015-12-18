from commands.cmds.BaseCommand import *
from packet.send import chat

class CommandHelp(BaseCommand):
    def __init__(self):
	    BaseCommand.__init__(self)
    def process(self, cmdobj):
	    chat(self, "hello, no help yet", 1)