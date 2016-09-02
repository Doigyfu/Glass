# coding=utf-8
from quarry.net.server import ServerFactory

from server_core.server import Mineserver


class Pureserver(Mineserver):
    def player_join_event(self):
        self.logger.info("hmm, it works!")

    def player_leave_event(self):
        self.logger.info("he leaved :(")


class MineFactory(ServerFactory):
    protocol = Pureserver


def main(args):
    # Parse options
    import optparse
    parser = optparse.OptionParser(usage="usage: %prog [options]")
    parser.add_option("-a", "--host", dest="host", default="", help="address to listen on")
    parser.add_option("-p", "--port", dest="port", default="25565", type="int", help="port to listen on")
    parser.add_option("-m", "--motd", dest="motd", default="PyMineserver: Test. Hello! Now with joining! §b§l\\o/§r",
                      type="string", help="motd to send to clients")
    parser.add_option("-o", "--offline", action="store_false", dest="auth", default=True,
                      help="offline mode does not authenticate players!")
    parser.add_option("-k", "--downtime", action="store_true", dest="down", default=False,
                      help="kick players with downtimemsg")
    parser.add_option("-q", "--downtimemsg", dest="downmsg",
                      default="Sorry, but this server is currently down for maintenance. Check back soon!",
                      help="message to kick for downtime with")
    parser.add_option("-w", "--wtitle", dest="wtitle", default="Welcome to Mineserver!",
                      help="title to display on join")
    parser.add_option("-s", "--wsubtitle", dest="wst", default="Enjoy this test server!",
                      help="subtitle to display on join")
    parser.add_option("-l", "--max-players", dest="maxplayers", default=20, help="max player count/limit")
    parser.add_option("-f", "--favicon", dest="favicon", default="creeper.png",
                      help="relative path to server favicon in png")
    global options
    (options, args) = parser.parse_args(args)

    # Warn about auth mode
    if options.auth:
        print(
            "Mineserver (warn/INFO)> Mineserver is running in online mode. All players must be authenticated to join. *(ONLINE)*")
    else:
        print(
            "Mineserver (WARN/info)> Mineserver is running in offline mode. Players can join with fake UUIDs and names without authentication! *[OFFLINE]*!")

    # Create factory
    factory = MineFactory()
    factory.motd = options.motd
    factory.online_mode = options.auth
    factory.favicon = options.favicon

    # Listen
    factory.listen(options.host, options.port)
    factory.run()


if __name__ == "__main__":
    print("Mineserver (warn/CRIT)> You should NOT be invoking this directly! Use mineserver.py.")
    exit(1)
