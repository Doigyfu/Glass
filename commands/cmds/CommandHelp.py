from commands.cmds.BaseCommand import *
from packet.send import chat

class cmd(BaseCommand):
    def process(self):
	    chat(self.cmdobj['scope'], "hello, no help yet :P coming soon!", 1)