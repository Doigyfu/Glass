import commands.cmds as cmds
from commands.cmds import CommandHelper

def handle(self, chat_raw):
    self.logger.info("Handling command: " + chatraw + " (for player" + self.fquid + ")")
    _atmp1 = chat_raw.split(" ")
    _atmp2 = list(_atmp1[0])
    del _atmp2[0]
    del _atmp1[0]
    cmdobj = {
        "base": _atmp2,
        "args_raw": _atmp1,
        "scope": self,
        "chat_raw": chat_raw
    }
   CommandHelper(cmds.InvalidCommand, cmdobj) if _atmp2 not in cmds.baseList else CommandHelper(cmds.baseList[_atmp2], cmdobj)