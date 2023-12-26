from datetime import datetime

def time_ago(timestamp: str) -> str:
    timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

    now = datetime.utcnow()
    delta = now - timestamp

    if delta.days == 0:
        if delta.seconds < 60:
            return 'just now'
        elif delta.seconds < 120:
            return '1 minute ago'
        elif delta.seconds < 3600:
            return f'{delta.seconds // 60} minutes ago'
        elif delta.seconds < 7200:
            return '1 hour ago'
        else:
            return f'{delta.seconds // 3600} hours ago'
    elif delta.days == 1:
        return 'yesterday'
    else:
        return f'{delta.days} days ago'