from io import TextIOBase, BufferedReader, StringIO, BytesIO


def get_stringio():
    return StringIO()

def get_bytesio():
    return BytesIO()


def reduce_fp(path, *args, **kwargs):
    if isinstance(path, str):
        return open(path, *args, **kwargs)
    elif isinstance(path, (TextIOBase, BufferedReader)):
        return path
    else:
        raise ValueError('Either file path or fp must be specified')
    

