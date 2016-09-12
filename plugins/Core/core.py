# Import plugin class
import time

from plugin_core import Plugin

# You SHOULD name instance of Plugin() as plugin, otherwise it wouldn't work!!!
plugin = Plugin(name="Core", description="Core plugin for server", version="")

plugin.log("Initialized successfully...")


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
