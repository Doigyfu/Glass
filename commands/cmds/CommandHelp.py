from commands.cmds import BaseCommand, CommandFactory
from packet.send import chat

class CommandHelp(BaseCommand):
    def __init__(self):
	    BaseCommand.__init__(self)
    def process(cmdobj):
	    chat(cmdobj[scope], "hello, no help yet", 1)