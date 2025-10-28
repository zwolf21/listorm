import jsonlines



def read_jsonline(file, mode='r', loads=None):
    with jsonlines.open(file, mode=mode, loads=loads) as fp:
        return list(fp)
