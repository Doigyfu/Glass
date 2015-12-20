from commands.cmds.CommandHelp import cmd
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
}