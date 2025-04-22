from datetime import datetime

def timestamp_formatter(timestamp: datetime) -> str:
    """format the timestamp to a standard format to YYYY-MM-DD hh:mm"""
    return timestamp.strftime('%Y-%m-%d %H:%M')