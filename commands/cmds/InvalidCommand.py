from commands.cmds import BaseCommand, CommandFactory, CommandHelper
from packet.send import chat

class InvalidCommand(BaseCommand):
    def process(cmdobj):
	    chat(cmdobj[scope], "\u00A7cInvalid command. Type /help for help.\u00A7r", 1)