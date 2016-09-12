# You can add new file as new plugin, or as addition(like there) - but, if you would do that, you need __init__.py:
from plugins.Example import plugin


# That's it!
@plugin.event("player_command")
def handle(player, command, args):
    if command == "example":
        player.send_chat("Yes, I'm here!")
