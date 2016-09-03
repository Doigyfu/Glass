# You must always import this
from yapsy.IPlugin import IPlugin


# And you must ALWAYS add IPlugin as base class to your's
class Plugin(IPlugin):
    #If you don't need to set your own long-living variables - you don't need __init__
    def __init__(self):
        super(Plugin, self).__init__()  # Call super's method in order to initialize plugin...
        # Then you can set your own stuff...
        self.hello_message = "Hello!!!"
        self.x = 0
        self.y = 0
        self.z = 0

    # Player argument must be ALWAYS present - it's player object
    def player_join_event(self, player):
        print(self.hello_message)
        print(player.username)

    def player_leave_event(self, player):
        print("goodbye from plug-in :(")
        print(player.username)

    # You need to add arguments to some event, this arguments will be in docs
    def player_move_event(self, player, x, y, z, on_ground):
        if (self.x - x) > 5:
            print("X delta is bigger than FIVE!")
        self.x = x
        self.y = y
        self.z = z

    def player_chat_event(self, player, message):
        print("player chat from plug-in " + str(message))

    def player_command_event(self, player, command, arguments):
        print("player command from plug-in " + str(arguments))
