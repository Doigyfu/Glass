from commands.cmds import BaseCommand
from packet.send import chat

class InvalidCommand(BaseCommand):
    def process(self, cmdobj):
	    chat(self, "\u00A7cInvalid command. Type /help for help.\u00A7r", 1)