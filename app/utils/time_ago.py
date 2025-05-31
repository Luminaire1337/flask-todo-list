from datetime import datetime
from typing import Union

def time_ago(timestamp: Union[str, datetime]) -> str:
    """
    Format a timestamp as a relative time string (e.g., "5 minutes ago").
    
    Args:
        timestamp: Datetime string or datetime object
        
    Returns:
        String describing the relative time
    """
    # Convert string to datetime if needed
    if isinstance(timestamp, str):
        try:
            timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return "invalid date"

    now = datetime.now()
    delta = now - timestamp

    # Handle future dates
    if delta.total_seconds() < 0:
        return "in the future"

    # Less than a minute
    if delta.days == 0 and delta.seconds < 60:
        return 'just now'
    
    # Less than an hour
    if delta.days == 0 and delta.seconds < 3600:
        minutes = delta.seconds // 60
        return f'{minutes} minute{"s" if minutes != 1 else ""} ago'
    
    # Less than a day
    if delta.days == 0:
        hours = delta.seconds // 3600
        return f'{hours} hour{"s" if hours != 1 else ""} ago'
    
    # Less than a week
    if delta.days < 7:
        return f'{delta.days} day{"s" if delta.days != 1 else ""} ago'
    
    # Less than a month
    if delta.days < 31:
        weeks = delta.days // 7
        return f'{weeks} week{"s" if weeks != 1 else ""} ago'
    
    # Format as regular date for older timestamps
    return timestamp.strftime('%b %d, %Y')