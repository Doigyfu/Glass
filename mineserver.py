#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is the new base initialization layer for Mineserver.
# Always call this instead of server_core/server.py
from server_core.server import *
import sys

main(sys.argv[1:])
