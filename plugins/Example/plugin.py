# You must always import this
from yapsy.IPlugin import IPlugin


# And you must ALWAYS add IPlugin as base class to your's
class Plugin(IPlugin):
    # If you don't need to set your global variables(across all players) - you don't need __init__
    def __init__(self):
        super(Plugin, self).__init__()  # Call super's method in order to initialize plugin...
        # Then you can set your own global variables (for all players)...

    # This is being called when plugin initializes..
    def activate(self):
        pass

    # This is being called when plugin shuts down..
    def deactivate(self):
        pass

    # Player argument must be ALWAYS present - it's player object
    # You can init player variables here (or in any another event)
    def player_join_event(self, player):
        player.x = 0
        player.y = 0
        player.z = 0
        print(player.username)

    def player_leave_event(self, player):
        print("goodbye from plug-in :(")
        print(player.username)

    # You need to add arguments to some event, this arguments will be in docs
    #So we check there if player movevent on X is bigger than 5 units
    def player_move_event(self, player, x, y, z, on_ground):
        if (player.x - x) > 3:
            print("X delta is bigger than FIVE!")
        # This variables are not equal for different players :)
        player.x = x
        player.y = y
        player.z = z

    def player_chat_event(self, player, message):
        print("player chat from plug-in " + str(message))

    def player_command_event(self, player, command, arguments):
        print("player command from plug-in " + str(arguments))
