from datetime import datetime, timezone
import pytz


def extract_time_from_unix(unix_timestamp):
    date_time = datetime.fromtimestamp(unix_timestamp, timezone.utc)
    time_only = date_time.time()

    seconds_since_midnight = time_only.hour * 3600 + time_only.minute * 60 + time_only.second

    return seconds_since_midnight


def unix_to_datetime(unix_timestamp):
    time_zone = pytz.FixedOffset(0)

    localized_time = datetime.fromtimestamp(unix_timestamp, tz=time_zone)

    return localized_time.strftime('%Y-%m-%d %H:%M:%S')
