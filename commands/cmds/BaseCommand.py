class BaseCommand():
    def begin(self, cmdobj):
        self.cmdobj = cmdobj
    	self.process()
    def process(self):
        pass
    def usage():
        return "this is an example command"