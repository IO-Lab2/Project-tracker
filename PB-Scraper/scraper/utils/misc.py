class HandlerNotFoundError(Exception):
    pass

def process_based_on_type(obj, handlers, default_handler=None):
    """
    Chooses a function handler from handlers based on obj's type. 
    Then calls the function handler with obj as its only argument

    handler functions should take only one argument - obj

    Parameters:
    obj (Any): The object to process.
    handlers (dict): A dictionary mapping types to their respective handler functions.
    default_handler (function, optional): A function to call if obj's type is not in handlers. Defaults to None.

    Returns:
    Any: The result of the handler function.

    Raises:
    HandlerNotFoundError: If obj's type does not match any handler and no default_handler is provided
    """
    obj_type = type(obj)
    if obj_type in handlers:
        return handlers[obj_type](obj)
    elif default_handler:
        return default_handler(obj)
    else:
        raise HandlerNotFoundError(f"process_based_on_type: type {obj_type} does not match any handler passed and no default_handler provided")


def get_by_keys(d:dict, keys, keep=True):
    '''
    d - dict
    keys - list: string keys to look for in d - keys that aren't in d are skipped
           or str: key
    keep - bool : if False removes returned keys from d

    returns a dict populated with keys (and their values) that are in d
    '''

    if not isinstance(keys, list):
        keys = [keys]

    extracted = dict()
    for key in keys:
        if not key in d:
            continue

        if keep:
            extracted[key] = d[key]
            continue

        extracted[key] = d.pop(key)
    return extracted


#adds parentheses around obj if it is a string - does nothing otherwise
def add_parenthesis(obj):
    if isinstance(obj, str):
        return "\"" + obj + "\""
    return obj


def filter_values(values, bools, include_removed=False):
    """
    Filters the values based on the corresponding boolean values.

    Parameters:
    values (list): A list of values.
    bools (list): A list of boolean values of the same length as 'values'.
    include_removed (bool): if true it will add removed values to return

    Returns:
    list: A list of values where the corresponding boolean value is True.
    tuple: if include_removed == True - a pair: (values after filtering, removed values)

    Raises:
    ValueError: if lengths of the two lists do not match
    """
    if len(values) != len(bools):
        raise ValueError("filter_values: the lengths of the two lists provided are not the same.")

    filtered_values = [value for value, flag in zip(values, bools) if flag]

    if not include_removed:
        return filtered_values

    removed_values = [value for value, flag in zip(values, bools) if not flag]
    return filtered_values, removed_values

