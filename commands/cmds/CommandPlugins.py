from packets.send import chat

from commands.cmds.BaseCommand import *


class cmd(BaseCommand):
    def process(self):
        self.osc = self.cmdobj['scope']
        chat(self.osc, self.jsconcat(), 1)
    def jsconcat(self):
        self.plugins = self.osc.plugins
        self.pcount = len(self.plugins)
        return "Plugins (" + str(self.pcount) + "): " + ", ".join(self.plugins)