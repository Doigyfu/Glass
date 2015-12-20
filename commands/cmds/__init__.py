from commands.cmds.CommandHelp import *
from commands.cmds.InvalidCommand import *
from commands.cmds.CommandPlugins import *
from commands.cmds.CommandStop import *
from commands.cmds.CommandFly import *
from commands.cmds.CommandGamemode import *
from commands.cmds.CommandGod import *

baseList = {
	"help": CommandHelp.cmd,
    "stop": CommandStop.cmd,
    "fly": CommandFly.cmd,
    "flight#a{fly}": CommandFly.cmd,
    "gamemode": CommandGamemode.cmd,
    "gm#a{gamemode}": CommandGamemode.cmd,
    "god": CommandGod.cmd,
    "godmode#a{god}": CommandGod.cmd
}