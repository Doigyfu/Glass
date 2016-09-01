from commands.cmds.BaseCommand import *
from packet.send import chat


class cmd(BaseCommand):
    def process(self):
        chat(self.cmdobj['scope'], "\u00A7cInvalid command. Type /help for help.\u00A7r", 1)
