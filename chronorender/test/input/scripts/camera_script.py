def render(rib, *args, **kwargs):
    print "hey"
    print "ARGS", args
    print "KWARGS", kwargs

    robj = kwargs['robj']
    print "ROBJ", robj

def render2(rib, *args, **kwargs):
    print "light"
