# coding=utf-8
from os.path import abspath

from plugin_core import PluginSystem
from .server import Mineserver, MineFactory

__all__ = ["main", "PureFactory", "Pureserver"]


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
    # Init plugin system
    factory.plugin_system = PluginSystem(folder=abspath('plugins'))
    # Search and register all event handlers
    factory.plugin_system.register_events()
    factory.listen(ip, port)
    print("(core.py) Server started, waiting for connections...")
    factory.run()


if __name__ == "__main__":
    print("You should NOT be invoking this directly! Use puremine.py.")
    exit(1)
