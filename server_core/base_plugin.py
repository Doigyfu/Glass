import logging

from yapsy.IPlugin import IPlugin


class BasePlugin(IPlugin):
    def __init__(self):
        super(BasePlugin, self).__init__()
        self.logger = logging.getLogger("%s plugin" % (self.__class__.__name__))
        self.logger.setLevel(logging.INFO)

    def player_join_event(self, player):
        pass

    def player_leave_event(self, player):
        pass

    def player_move_event(self, player, x, y, z, on_ground):
        pass

    def player_chat_event(self, player, message):
        pass

    def player_command_event(self, player, command, arguments):
        pass
