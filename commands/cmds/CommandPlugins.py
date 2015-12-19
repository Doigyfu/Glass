from commands.cmds.BaseCommand import *
from packet.send import chat

class cmd(BaseCommand):
    def process(self):
	    chat(self.cmdobj['scope'], self.jsconcat(), 1)
    def jsconcat(self):
        return "Plugins (" + self.pcount or 0 + "): "