# coding=utf-8
from os.path import abspath

from plugin import PluginSystem
from server import Mineserver, MineFactory

__all__ = ["main", "PureFactory", "Pureserver"]

server_config = '''
#Puremine server properties
#File format is same with Bukkit/Spigot servers
#However, not all values are supported, so many of them just ignored
generator-settings=
op-permission-level=4
allow-nether=true
level-name=world
enable-query=false
allow-flight=false
announce-player-achievements=true
server-port=25565
max-world-size=29999984
level-type=DEFAULT
enable-rcon=false
level-seed=
force-gamemode=false
server-ip=127.0.0.1
network-compression-threshold=256
max-build-height=256
spawn-npcs=true
white-list=false
spawn-animals=true
hardcore=false
snooper-enabled=true
resource-pack-sha1=
online-mode=false
resource-pack=
pvp=true
difficulty=1
enable-command-block=false
gamemode=0
player-idle-timeout=0
max-players=500
max-tick-time=60000
spawn-monsters=true
generate-structures=true
view-distance=10
motd=Puremine (Python powered)'''


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
    print("(start.py) Server started, waiting for connections...")
    factory.run()


def str2bool(string):
    trues = ('True', 'true')
    falses = ('False', 'false')
    if string in trues:
        return True
    elif string in falses:
        return False
    else:
        raise TypeError("String {0} isn't a boolean!".format(string))


def create_config():
    try:
        with open('server.properties', 'w') as config:  # Let's create it!
            config.write(server_config)
    except IOError:
        print("Config file not created (maybe I don't have write access to directory?)")


def read_config():
    properties = {}  # Dict for configuration
    try:
        with open('server.properties') as config:
            for line in config.readlines():
                if not line.startswith("#"):  # If line isn't a comment
                    key, value = line.strip().split('=')  # Split key and value
                    if value:  # If value isn't empty
                        if value in ('True', 'false', 'true', 'False'):  # If line is a boolean
                            properties[key] = str2bool(value)  # Add key and value to our dictionary
                            continue
                        elif value.isdigit():  # If line is a number
                            properties[key] = int(value)
                            continue
                        else:
                            properties[key] = value
        return properties
    except IOError:  # If there's no config file
        print("Config file don't found, creating...")
        create_config()


if __name__ == '__main__':
    props = read_config()
    main(props)
