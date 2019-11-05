from datetime import datetime, timezone


class TimestampConverter:
    MICROSECONDS_PER_MILLISECOND = 1000
    MILLISECONDS_PER_SECOND = 1000
    MILLISECONDS_PER_MINUTES = 60 * MILLISECONDS_PER_SECOND
    MILLISECONDS_PER_HOURS = 60 * MILLISECONDS_PER_MINUTES
    MILLISECONDS_PER_DAY = 24 * MILLISECONDS_PER_HOURS

    @staticmethod
    def get_datetime_from_timestamp(timestamp_with_milliseconds):
        milliseconds = timestamp_with_milliseconds % TimestampConverter.MILLISECONDS_PER_SECOND
        timestamp = timestamp_with_milliseconds // TimestampConverter.MILLISECONDS_PER_SECOND

        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        dt = dt.replace(microsecond=int(milliseconds * TimestampConverter.MICROSECONDS_PER_MILLISECOND))

        return dt

    @staticmethod
    def get_timestamp_from_datetime(dt):
        return int(dt.timestamp() * TimestampConverter.MILLISECONDS_PER_SECOND)

    @staticmethod
    def get_timestamp_with_zeroed_time(timestamp_with_milliseconds):
        """Gets timestamp with the start time of the day (00:00:00) from any timestamp with milliseconds

        Args:
             timestamp_with_milliseconds (int): timestamp with milliseconds
        Returns:
             timestamp_with_milliseconds (int): timestamp of the start time of the day with milliseconds
        """
        timestamp_with_milliseconds -= timestamp_with_milliseconds % TimestampConverter.MILLISECONDS_PER_DAY

        return timestamp_with_milliseconds

    @staticmethod
    def get_timestamp_plus_one_day(timestamp_with_milliseconds):
        return int(timestamp_with_milliseconds + TimestampConverter.MILLISECONDS_PER_DAY)
