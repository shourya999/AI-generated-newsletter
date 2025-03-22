from datetime import datetime

def get_timestamp():
    """Return a formatted timestamp string for the current time."""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")