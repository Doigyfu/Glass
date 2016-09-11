# Import plugin class
from plugin_core import Plugin

# You SHOULD name instance of Plugin() as plugin, otherwise it wouldn't work!!!
plugin = Plugin(name="Core", description="Core plugin for server", version="0.1a")

plugin.logger.info("Initialized successfully...")


@plugin.event("player_command")
def command(player, command, arguments):
    if command == "stop":
        from twisted.internet import reactor  # Import reactor and call stop methods
        reactor.removeAll()
        reactor.iterate()
        reactor.stop()
