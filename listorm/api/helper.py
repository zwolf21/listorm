from ..utils import get_argcounts


def reduce_callable(value, *args, **kwargs):
    if callable(value):
        return value(*args, **kwargs)
    return value


def reduce_args_count(app, *args):
    if callable(app):
        args_count = get_argcounts(app)
        if args_count > 2:
            raise ValueError("{} can have no more than 2 args.".format(app))
        return app(*args[:args_count])
    return app


def reduce_where(where):
    return where or (lambda x: True)