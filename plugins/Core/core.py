# Import plugin class
import time

from plugin_core import Plugin

# You SHOULD name instance of Plugin() as plugin, otherwise it wouldn't work
plugin = Plugin(name="Core", description="Core plugin for server (containts all basic stuff)", version="0.1")

# You can do this to make code shorter and cleaner
event = plugin.event

plugin.log("Initialized successfully...")


@event("player_command")
def handler(player, command, args):
    if command == "stop":
        player.send_chat("Server stopping... You will be kicked in two seconds")
        time.sleep(2)
        plugin.log(player.nickname + " has stopped the server!")
        from twisted.internet import reactor  # Import reactor and call stop methods
        reactor.removeAll()
        reactor.iterate()
        reactor.stop()
    if command == "tppos":
        # If command called with 3 arguments
        if len(args) == 3:
            # Set player position
            try:
                x, y, z = [float(arg) for arg in args]  # Convert strings to floats
                player.set_position(x, y, z)
                player.send_chat("Teleported to X:%f Y:%f Z:%f successfully" % (x, y, z))
            except ValueError:  # If we can't convert it
                player.send_chat("You need to supply numbers!")
        else:
            player.send_chat("tppos takes 3 arguments: x,y,z")
    if command == "help":
        # TODO: Make something useful here
        player.send_chat("There's nothing here, sorry :(")


# You can handle one event how many times do you want!
@event("player_command")
def broadcast(player, command, args):
    if command == "broadcast":
        if args:
            message = ' '.join(args)  # Join all arguments in one message
            player.send_chat_all("SERVER BROADCAST: " + message)
        else:
            player.send_chat("You need to supply at least one argument for string! e.g - /broadcast hello")
