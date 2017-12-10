from datetime import datetime

def jstime_to_datetime(jstime):
    return datetime.fromtimestamp(jstime / 1000)

def time_to_json(data):
    for key in data:
        if isinstance(data[key], datetime):
            data[key] = data[key].isoformat()
    return data