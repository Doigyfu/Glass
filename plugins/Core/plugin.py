# You must always import base plugin like this, otherwise it won't work

import server_core.base_plugin as base


# You must inherit from base plugin like that
class Plugin(base.BasePlugin):
    def player_command_event(self, player, command, arguments):
        if command == "plugins":  # Plugins command
            # Plugin info stored in player.factory.plugin_infos - dict
            for name, description in player.factory.plugin_infos.iteritems():
                player.send_chat(name + " -> " + description)  # Send info about plugins to player
        if command == "stop":
            from twisted.internet import reactor  # Import reactor and call stop methods
            reactor.removeAll()
            reactor.iterate()
            reactor.stop()
