# coding=utf-8
from server_core.server import Mineserver, MineFactory


class Pureserver(Mineserver):
    def player_join_event(self):
        self.logger.info("hmm, it works!")
    def player_leave_event(self):
        self.logger.info("he leaved :(")


class PureFactory(MineFactory):
    protocol = Pureserver
    max_players = 100
    online_mode = False


def main():
    factory = PureFactory()
    factory.motd = "Pureserver test"
    factory.online_mode = False

    # Listen
    factory.listen('127.0.0.1', 25565)
    factory.run()


if __name__ == "__main__":
    print("Puremine (warn/CRIT)> You should NOT be invoking this directly! Use puremine.py.")
    exit(1)
