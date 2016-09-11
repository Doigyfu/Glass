#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This code was originally taken from https://github.com/zeuxisoo/python-pluginplot
import logging

__all__ = ['Plugin']


class Plugin(object):
    def __init__(self, name="Plugin", description="Most awesome standart description!", version="1.3.3.7"):
        self.deferred_events = []
        self.name = name
        self.description = description
        self.version = version
        # Create logger
        self.logger = logging.getLogger("{0} v{1}".format(self.name, self.version))
        self.logger.setLevel(logging.INFO)

    # Event wrapper
    def event(self, name=None):
        def wrapper(method):
            self.add_deferred_method(name, method)
            return method

        return wrapper

    def add_deferred_method(self, name, method):
        if name is None:
            name = method.__name__
        self.deferred_events.append(lambda target: target.add_event(name, method))

    # Register event
    def register(self, plugin):
        for deferred_event in self.deferred_events:
            deferred_event(plugin)
