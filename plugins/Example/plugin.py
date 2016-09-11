# You must always import base plugin like this, otherwise it won't work

from plugin_core import Plugin

# You can optionally enter the name of your plugin, description, and version
plugin = Plugin(name="Example plugin", description="Example plugin for developers", version="0.1alpha")

# You can init your global variables anywhere (except functions, of course), for example here:
test = 1
plugin.logger.info("Initialized successfully...")


@plugin.event("player_join")
# You can name event handler functions with ANY name
# Player argument must be ALWAYS present - it's player object
def player_join_event(player):
    # You can add variables for player object
    player.x = 0
    player.y = 0
    player.z = 0
    # The default logger is plugin | LOG_LEVEL | message
    plugin.logger.info(player.username)


@plugin.event("player_leave")
def player_leave_event(player):
    plugin.logger.info("goodbye from plug-in :(")


@plugin.event("player_move")
def player_move_event(player, x, y, z, on_ground):
    # This variables are not equal for different players
    # If player moved on more than 5 x coord let's write in log
    if abs(player.x - x) > 5:
        plugin.logger.info("X delta is bigger than five")
    player.x = x
    player.y = y
    player.z = z


@plugin.event("player_chat")
def player_chat_event(player, message):
    plugin.logger.info("player chat from plug-in " + str(message))


@plugin.event("player_command")
def player_command_event(player, command, arguments):
    plugin.logger.info("player command from plug-in " + str(arguments))
