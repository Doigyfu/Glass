def pushChat(msga, t):
    global eobj_byid
    acount = 0
    for pobja in eobj_byid:
        p.chat(eobj_byid[pobja], msga, t)
        if acount != 1:
            eobj_byid[pobja].logger.info("[CHAT] " + msga)
            acount = 1


def pushChatCall(msga, t, cfn):
    global eobj_byid
    acount = 0
    for pobja in eobj_byid:
        p.chat(eobj_byid[pobja], msga, t)
        if acount != 1:
            eobj_byid[pobja].logger.info("[CHAT] " + msga)
            acount = 1
    cfn()