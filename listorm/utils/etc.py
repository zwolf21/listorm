def tuplize(arg):
    if arg is None:
        return arg
    if isinstance(arg, (list, tuple)):
        return tuple(arg)
    return arg,