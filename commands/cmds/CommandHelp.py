from commands.cmds.BaseCommand import *
from packet.send import chat_json

class cmd(BaseCommand):
    def process(self):
        self.pages = 1
        chat_json(self.cmdobj['scope'], self.jsconcat(), 1)
    def jsconcat(self):
        try:
            self.pagenm = self.cmdobj['args_raw'][0]
        except IndexError:
            self.pagenm = "1"
        return {
            "text": "",
            "extra": [{
                "text": "---------",
                "color": "yellow"
            }, {
                "text": " Help: Index (" + self.pagenm + "/" + str(self.pages) + ") "
            }, {
                "text": "---------------------",
                "color": "yellow"
            }, {
                "text": "\nUse /help [",
                "color": "gray"
            }, {
                "text": "n",
                "color": "gray",
                "italic": True
            }, {
                "text": "] to get page ",
                "color": "gray"
            }, {
                "text": "n",
                "color": "gray",
                "italic": True
            }, {
                "text": " of help.",
                "color": "gray"
            }, {
                "text": "\nMineserver: ",
                "color": "gold"
            }, {
                "text": "All commands for Mineserver"
            }, {
                "text": "\n/help: ",
                "color": "gold"
            }, {
                "text": "Shows the help menu"
            }, {
                "text": "\n/plugins: ",
                "color": "gold"
            }, {
                "text": "Get a list of plugins running on the server"
            }, {
                "text": "\n--------------------------------------------",
                "color": "yellow"
            }]
        }