from server import players


def pushChat(self, message, position):
    acount = 0
    for pobja in self.eobj_byid:
        p.chat(self.eobj_byid[pobja], message, position)
        if acount != 1:
            self.eobj_byid[pobja].logger.info("[CHAT] " + msga)
            acount = 1


def pushChatCall(self, message, position=0):
    acount = 0
    for player in self.players:
        p.chat(self.players[player], message, t)
        if acount != 1:
            self.eobj_byid[pobja].logger.info("[CHAT] " + msga)


def global_chat(message):
    for entity_id, player_object in players.iteritems():
        player_object.logger.info(message)

# import commands.cmds as cmds

def handle_command(self, command_string):
    self.logger.info("Player " + self.username + " issued server command: " + command_string)
    command_list = command_string.split(" ")  # Command list - e.g ['/login','123123123','123123123']
    command, arguments = command_list[0], command_string.split(" ")[1:]  # Get command and arguments
    print(command, arguments)
    cmdobj = {
        "command": command,
        "args_raw": arguments,
        # "scope": self,
        "chat_raw": chat_message
    }
    # if command not in cmds.baseList: cmds.InvalidCommand.cmd.begin(cmds.InvalidCommand.cmd(), cmdobj)
    # else: cmds.baseList[command].begin(cmds.baseList[command](), cmdobj)

#print(handle_command("/login 123123123 123123123"))
