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


def main():
    factory = MineFactory()
    factory.motd = "Pureserver test"
    factory.online_mode = False

    # Listen
    factory.listen('127.0.0.1', 25565)
    factory.run()


if __name__ == "__main__":
    print("Mineserver (warn/CRIT)> You should NOT be invoking this directly! Use puremine.py.")
    exit(1)
