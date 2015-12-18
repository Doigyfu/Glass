from commands.cmds import BaseCommand

def CommandHelper(subcmdclass, cmdobj):
    cmdinstance = CommandFactory()
    cmdinstance.command = subcmdclass
    cmdinstance.start(cmdobj)
    

class CommandFactory(command.Factory, object):
    command = BaseCommand
    
    def start(cmdobj):
        cmdinst = command()
        cmdinst.process(cmdobj)