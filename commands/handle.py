import commands.cmds as cmds

def handle(self, chat_raw):
    self.logger.info("Player " + self.username + " issued server commnd: " + chat_raw)
    _atmp1 = chat_raw.split(" ")
    _atmp2 = list(_atmp1[0])
    del _atmp2[0]
    del _atmp1[0]
    _atmp3 = "".join(_atmp2)
    cmdobj = {
        "base": _atmp3,
        "args_raw": _atmp1,
        "scope": self,
        "chat_raw": chat_raw
    }
    if _atmp3 not in cmds.baseList: cmds.InvalidCommand.cmd.begin(cmds.InvalidCommand.cmd(), cmdobj)
    else:
        cmds.baseList[c].begin(cmds.baseList[_atmp3](), cmdobj)
