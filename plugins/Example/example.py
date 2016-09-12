# You must always import base plugin like this, otherwise it won't work

from plugin_core import Plugin

# You can optionally enter the name of your plugin, description, and version
plugin = Plugin(name="Example plugin", description="Example plugin for developers", version="0.1alpha")

# You can init your global variables anywhere (except functions, of course), for example here:
test = 1
plugin.log("Initialized successfully...")
@plugin.event("player_join")
# You can name event handler functions with ANY name
# Player argument must be ALWAYS present - it's player object
def join(player):
    # You can add variables for player object
    player.x = 0
    player.y = 0
    player.z = 0
    # The default logger is plugin | LOG_LEVEL | message
    plugin.log(player.username)


@plugin.event("player_leave")
def leave(player):
    plugin.log("Goodbye from plugin , %s :(" % player.nickname)


@plugin.event("player_move")
def move(player, x, y, z, on_ground):
    # This variables are not equal for different players
    # If player moved on more than 7 x coord let's write in log
    # Player.position is Position() class from types.py
    if abs(player.position.x - x) > 7:
        plugin.log("X delta is bigger than seven")
        print(player.position)


@plugin.event("player_chat")
def chat(player, message):
    plugin.log("Player chat event from example plugin -> %s %s" % (player.nickname, message))


@plugin.event("player_command")
def command(player, command, args):
    plugin.log("Player command event from example plugin %s with args-> %s" % (command, str(args)))
