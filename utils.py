from datetime import datetime

def int_to_datetime(time):
    """
    :param data: timestamp to parse time object.

    parse integer timestamp to Date instance.
    """
    return datetime.fromtimestamp(time)

def time_to_json(data):
    """
    :param data: time data to parse.
    
    formats the time fields in order the parse to json.
    """
    for key in data:
        if isinstance(data[key], datetime):
            data[key] = data[key].isoformat()
    return data