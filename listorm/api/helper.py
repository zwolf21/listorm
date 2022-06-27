def reduce_callable(value, *args, **kwargs):
    if callable(value):
        return value(*args, **kwargs)
    return value

