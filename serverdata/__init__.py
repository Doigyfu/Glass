# -*- coding: utf-8 -*-

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
