'''from commands.cmds.CommandHelp import cmd
from commands.cmds.InvalidCommand import cmd
from commands.cmds.CommandPlugins import cmd
from commands.cmds.CommandStop import cmd
from commands.cmds.CommandFly import cmd
from commands.cmds.CommandGamemode import cmd
from commands.cmds.CommandGod import cmd

baseList = {
	"help": CommandHelp.cmd,
    "stop": CommandStop.cmd,
    "fly": CommandFly.cmd,
    "flight#a{fly}": CommandFly.cmd,
    "gamemode": CommandGamemode.cmd,
    "gm#a{gamemode}": CommandGamemode.cmd,
    "god": CommandGod.cmd,
    "godmode#a{god}": CommandGod.cmd,
    "plugins": CommandPlugins.cmd
}'''

import os  # For list directory files

for module in os.listdir(os.path.dirname(__file__)):  # Search all files in a current directory
    if module == '__init__.py' or module[
                                  -3:] != '.py':  # If it is a init or not python script - go to the next iteration
        continue
    __import__(module[:-3], locals(), globals())  # Import module
