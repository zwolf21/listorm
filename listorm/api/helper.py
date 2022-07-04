from ..utils import get_argcounts, filer_kwargs



def reduce_args_count(app, *args):
    if callable(app):
        args_count = get_argcounts(app)
        if args_count > 2:
            raise ValueError("{} can have no more than 2 args.".format(app))
        return app(*args[:args_count])
    return app


def reduce_where(item, where):
    if where is None:
        return True
    
    if not callable(where):
        raise ValueError('where must be callable')
    
    try:
        return where(**item)
    except TypeError:
        kwargs = filer_kwargs(item, where)
        return where(**kwargs)



def reduce_callback(item, key, app):
    updated = {}
    if not callable(app):
        updated[key] = app
    else:
        try:
            kwargs = filer_kwargs(item, app)
        except ValueError:
            updated[key] = app(item[key])
        else:
            try:
                updated[key] = app(**item)
            except TypeError:
                if kwargs:
                    updated[key] = app(**kwargs)
                else:
                    updated[key] = app(item[key])
    
    return updated
