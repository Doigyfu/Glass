# You must always import base plugin like this, otherwise it won't work

from plugin import Plugin

# You can optionally enter the name of your plugin, description, and version
plugin = Plugin(name="Example plugin", description="Example plugin for developers")

# You can init your global variables anywhere (except functions, of course), for example here:
test = 1

# For simpler usage you can assign plugin.event to variable
event = plugin.event

plugin.log("Initialized successfully")


@event("player_join")
# You can name event handler functions with ANY name
# Player argument must be ALWAYS present - it's player object
def join(player):
    # You can add variables for player object
    player.x = 0
    player.y = 0
    player.z = 0
    # The default logger is plugin | LOG_LEVEL | message
    plugin.log("Wow, {name} joined the server!".format(name=player.username))


@event("player_leave")
def he_leaved(player):
    plugin.log("Goodbye from plugin , {username} :(".format(username=player.nickname))


@event("player_move")
def moved(player, x, y, z, on_ground):
    # This variables are not equal for different players
    # If player moved on more than 7 x coord let's write in log
    if abs(player.position.x - x) > 7:
        plugin.log("X delta is bigger than seven")
        # Player.position is Position() class from values.py
        print(player.position)


@event("player_chat")
def chatmsg(player, message):
    plugin.log("Player chat event from example plugin -> {0} {1}".format(player.nickname, message))


@event("player_command")
def cmd(player, command, args):  # That's it!
    if command == "example":
        player.send_chat("Yes, I'm here!")
    plugin.log("Player command event from example plugin -> command {0} with args-> {1}".format(command, str(args)))
