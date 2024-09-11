from datetime import datetime

import pytz


class TimeService:

    def unix_to_time(self, unix_timestamp):
        timezone = pytz.FixedOffset(0)

        localized_time = datetime.fromtimestamp(unix_timestamp, tz=timezone)

        return localized_time.strftime('%H:%M:%S')

    def unix_to_datetime(self, unix_timestamp):
        timezone = pytz.FixedOffset(0)

        localized_time = datetime.fromtimestamp(unix_timestamp, tz=timezone)

        return localized_time.strftime('%Y-%m-%d %H:%M:%S')
