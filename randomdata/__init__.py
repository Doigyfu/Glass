# -*- coding: utf-8 -*-
idcounter = -1

def join_json(self):
    return {
            'text': "",
            'extra': [{
                'text': "**",
                'obfuscated': True
            }, {
                'text': " "
            }, {
                'text': "Welcome, player",
                'color': "gold",
                'bold': True
            }, {
                'text': " "
            }, {
                'text': self.username,
                'underlined': True,
                'color': "red"
            }, {
                'text': "!",
                'italic': True,
                'color': "light_purple"
            }, {
                'text': " "
            }, {
                'text': "Type ",
                'italic': True
            }, {
                'text': "/help",
                'italic': True,
                'underlined': True
            }, {
                'text': " "
            }, {
                'text': "for more info.",
                'italic': True
            }, {
                'text': " "
            }, {
                'text': "**",
                'obfuscated': True
            }, {
                'text': '\n'
            }]
        }


def getFreeId():
    global idcounter
    idcounter += 1
    return idcounter


def help_json(self):
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
                "text": "\n--------------------",
                "color": "yellow"
            }, {
                "text": "««",
                "color": "green",
                "hoverEvent": {
                    "action": "show_text",
                    "value": {
                        "text": "« Previous Page",
                        "color": "gold",
                        "italic": True
                    }
                }
            }, {
                "text": " 1 ",
                "color": "yellow"
            }, {
                "text": "»»",
                "color": "green",
                "hoverEvent": {
                    "action": "show_text",
                    "value": {
                        "text": "Next Page »",
                        "color": "gold",
                        "italic": True
                    }
                }
            }, {
                "text": "-------------------",
                "color": "yellow"
            }]
        }


def chunks(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]