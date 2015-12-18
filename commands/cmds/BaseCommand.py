class BaseCommand(object):
    usage = "this is an example command"

    def begin(self, cmdobj):
        self.cmdobj = cmdobj
    	self.process()
    def process(self):
        pass