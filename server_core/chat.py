import packet as p

def pushChat(eobj_byid, msga, t):
    acount = 0
    for pobja in eobj_byid:
        p.chat(eobj_byid[pobja], msga, t)
        if acount != 1:
            eobj_byid[pobja].logger.info("[CHAT] " + msga)
            acount = 1


def pushChatCall(eobj_byid, msga, t, cfn):
    acount = 0
    for pobja in eobj_byid:
        p.chat(eobj_byid[pobja], msga, t)
        if acount != 1:
            eobj_byid[pobja].logger.info("[CHAT] " + msga)
            acount = 1
    cfn()
