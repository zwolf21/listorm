import functools



def reduce_kwargs(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        params = {
            key: value
            for arg in args if isinstance(arg, dict)
            for key, value in arg.items()
        }
        params.update(kwargs)
        return func(self, *args, **params)
    return wrapper



def reduce_args(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        _args = []
        for arg in args:
            if isinstance(arg, (list, tuple)):
                _args += arg
            else:
                _args.append(arg)
        return func(self, *_args, **kwargs)
    return 