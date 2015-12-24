import packet as p

def pushChat(self, msga, t):
    acount = 0
    for pobja in self.eobj_byid:
        p.chat(self.eobj_byid[pobja], msga, t)
        if acount != 1:
            self.eobj_byid[pobja].logger.info("[CHAT] " + msga)
            acount = 1


def pushChatCall(self, msga, t, cfn):
    acount = 0
    for pobja in self.eobj_byid:
        p.chat(self.eobj_byid[pobja], msga, t)
        if acount != 1:
            self.eobj_byid[pobja].logger.info("[CHAT] " + msga)
            acount = 1
    cfn()
