def _route_callable(value, *args, **kwargs):
    if isinstance(value, callable):
        return value(*args, **kwargs)
    return value

