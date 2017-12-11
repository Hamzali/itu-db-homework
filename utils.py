from datetime import datetime

def int_to_datetime(time):
    return datetime.fromtimestamp(time)

def time_to_json(data):
    for key in data:
        if isinstance(data[key], datetime):
            data[key] = data[key].isoformat()
    return data