import gc, logging, sys, types

def get_refcounts():
    d = {}
    sys.modules
    # collect all classes
    for m in sys.modules.values():
        for sym in dir(m):
            o = getattr (m, sym)
            if type(o) is types.ClassType:
                d[o] = sys.getrefcount (o)
    # sort by refcount
    pairs = map (lambda x: (x[1],x[0]), d.items())
    pairs.sort()
    pairs.reverse()
    return pairs

def print_refs():
    for n, c in get_refcounts():
        print '%10d %s' % (n, c.__name__)

def print_garbage():
    if __debug__:
        print '>'*30
        gc.collect()
        print "gc garbage:", gc.garbage
        print_refs()
        print '>'*30

def log_garbage():
    if __debug__:
        log = logging.getLogger("garbage")
        log.debug('>'*30)
        gc.collect()
        log.debug("gc garbage: %s" % gc.garbage)
        print_refs()
        log.debug('>'*30)
