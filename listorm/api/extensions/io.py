import os
from io import TextIOBase, BufferedReader, StringIO, BytesIO


def get_stringio(*args):
    return StringIO(*args)

def get_bytesio(*args):
    return BytesIO(*args)


def reduce_fp(path=None, content=None, *args, **kwargs):
    if path:
        if isinstance(path, str):
            return open(path, *args, **kwargs)
        elif isinstance(path, (TextIOBase, BufferedReader)):
            return path
        else:
            raise ValueError('Either file path or fp must be specified')
    elif content:
        if isinstance(content, str):
            return get_stringio(content)
        return get_bytesio(content)


def reduce_excel_input(file):
    if isinstance(file, str):
        with open(file, 'rb') as fp:
            return BytesIO(fp.read())
    elif isinstance(file, bytes):
        return BytesIO(file)
    elif isinstance(file, BufferedReader):
        return file
    else:
        raise ValueError('Invalid excel file types')

