from datetime import datetime

def current_timestamp():
    return int(datetime.now().timestamp())

def current_timestamp_mili():
    return int(datetime.now().timestamp() * 1000)