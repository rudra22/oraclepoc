def file_type(file_name):
    if file_name.lower().endswith('yaml') or file_name.lower().endswith('yml'):
        return 'yml'
    elif file_name.lower().endswith('json'):
        return 'json'
    else:
        return file_name.lower().split('.')[-1]


def safe_get(collection, key, default=None, raise_exception=True):
    try:
        ret_val = collection.get(key, default)
        if not ret_val and raise_exception:
            raise ValueError
    except Exception as e:
        raise Exception("Error fetching key {}. {}".format(key, repr(e)))
    return ret_val


def coalesce(*values):
    return next((v for v in values if v is not None), None)
