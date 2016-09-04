# coding=utf-8

from server_core.server import Mineserver, MineFactory


class Pureserver(Mineserver):
    def player_join_event(self):
        pass

    def player_leave_event(self):
        pass


class PureFactory(MineFactory):
    protocol = Pureserver


def main(properties_dict):
    factory = PureFactory()
    factory.motd = properties_dict.get("motd", "Pureserver test")
    factory.online_mode = properties_dict.get("online-mode", False)
    factory.max_players = properties_dict.get("max-players", 20)
    factory.compression_threshold = properties_dict.get("network-compression-threshold", 256)
    ip = properties_dict.get("server-ip", "127.0.0.1")
    port = properties_dict.get("server-port", 25565)
    #    factory.
    ###INIT PLUGIN SYSTEM
    factory.plugins = []
    from yapsy.PluginManager import PluginManager, PluginFileLocator
    pm = PluginManager()
    pl = PluginFileLocator()
    pl.setPluginInfoExtension("info")
    pm.setPluginLocator(pl)
    pm.setPluginPlaces(["./plugins"])
    pm.collectPlugins()
    plugins = []
    factory.plugins = []
    for pluginInfo in pm.getAllPlugins():
        plugins.append(pluginInfo)
    factory.plugin_infos = {}
    for plugin in plugins:
        factory.plugin_infos[plugin.name] = plugin.description
        plugin = plugin.plugin_object
        factory.plugins.append(plugin)
    ###PLUGIN INFOS ARE STORED IN PLUGINS LIST NOW
    # Listen
    factory.listen(ip, port)
    factory.run()


if __name__ == "__main__":
    print("Puremine (warn/CRIT)> You should NOT be invoking this directly! Use puremine.py.")
    exit(1)
