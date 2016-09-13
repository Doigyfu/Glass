# Import plugin class
import time

from plugin_core import Plugin

# You SHOULD name instance of Plugin() as plugin, otherwise it wouldn't work!!!
plugin = Plugin(name="Core", description="Core plugin for server", version="")



@plugin.event("player_command")
def command(player, command, args):
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
                x, y, z = [float(arg) for arg in args]
                player.set_position(x, y, z)
                player.send_chat("Teleported to X:%f Y:%f Z:%f successfully" % (x, y, z))
            except ValueError:
                player.send_chat("You need to supply numbers!")
        else:
            player.send_chat("tppos takes 3 arguments: x,y,z")
    if command == "help":
        player.send_chat("There's nothing here, sorry :(")


# You can handle one event how many times do you want!
@plugin.event("player_command")
def broadcast(player, command, args):
    if command == "broadcast":
        try:
            message = ' '.join(args)
            player.send_chat_all("SERVER BROADCAST: " + message)
        except:
            player.send_chat("You need to supply one argument - message (/broadcast message asd asd ")
