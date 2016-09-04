# You must always import base plugin like this, otherwise it won't work

import server_core.base_plugin as base


# You must inherit from base plugin like that
class Plugin(base.BasePlugin):
    # You can init your global variables here
    def __init__(self):
        super(Plugin, self).__init__()
        self.test = 1

    # Player argument must be ALWAYS present - it's player object
    # You can init player variables here (or in any another event)
    def player_join_event(self, player):
        player.x = 0
        player.y = 0
        player.z = 0
        # The default logger is <name of plugin> plugin | LOG_LEVEL | message
        self.logger.info(player.username)

    def player_leave_event(self, player):
        self.logger.info("goodbye from plug-in :(")

    # You need to add arguments to some event, this arguments will be in docs
    def player_move_event(self, player, x, y, z, on_ground):
        # This variables are not equal for different players :)
        # If player moved on more than 2 x let's write in chat
        if abs(player.x - x) > 5:
            self.logger.info("X delta is bigger than five")
        player.x = x
        player.y = y
        player.z = z

    def player_chat_event(self, player, message):
        self.logger.info("player chat from plug-in " + str(message))

    def player_command_event(self, player, command, arguments):
        self.logger.info("player command from plug-in " + str(arguments))
