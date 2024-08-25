from datetime import datetime, timezone


def get_time_difference(start_time):
    time_difference = datetime.now(timezone.utc) - start_time

    return time_difference.total_seconds()
