# -*- coding: utf-8 -*-
from commands.cmds.BaseCommand import *
from packet.send import chat_json
from randomdata import help_json


class cmd(BaseCommand):
    def process(self):
        self.pages = 1
        chat_json(self.cmdobj['scope'], self.jsconcat(), 1)

    def jsconcat(self):
        try:
            self.pagenm = self.cmdobj['args_raw'][0]
        except IndexError:
            self.pagenm = "1"
        return help_json(self)
