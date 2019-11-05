import unittest
from timestamp_converter import TimestampConverter


class TimestampConverterTestCase(unittest.TestCase):
    def test_timestamp_is_correctly_converted(self):
        # 2019 Oct 19 01:36:39 UTC
        timestamp = 1571448999
        milliseconds = 423
        timestamp_with_milliseconds = int(timestamp * TimestampConverter.MILLISECONDS_PER_SECOND + milliseconds)

        dt = None

        with self.subTest(name='get datetime from timestamp with milliseconds'):
            dt = TimestampConverter.get_datetime_from_timestamp(timestamp_with_milliseconds)

            self.assertEqual(2019, dt.year)
            self.assertEqual(10, dt.month)
            self.assertEqual(19, dt.day)

            self.assertEqual(1, dt.hour)
            self.assertEqual(36, dt.minute)
            self.assertEqual(39, dt.second)
            self.assertEqual(milliseconds * TimestampConverter.MICROSECONDS_PER_MILLISECOND, dt.time().microsecond)

        with self.subTest(name='get timestamp from datetime with milliseconds'):
            new_timestamp = TimestampConverter.get_timestamp_from_datetime(dt)

            self.assertEqual(timestamp_with_milliseconds, new_timestamp)

        timestamp_with_zeroed_time = None

        with self.subTest(name='get timestamp with zeroed time'):
            timestamp_with_zeroed_time = TimestampConverter.get_timestamp_with_zeroed_time(timestamp_with_milliseconds)

            self.assertEqual(1571443200000, timestamp_with_zeroed_time)

            new_dt = TimestampConverter.get_datetime_from_timestamp(timestamp_with_zeroed_time)

            self.assertEqual(2019, new_dt.year)
            self.assertEqual(10, new_dt.month)
            self.assertEqual(19, new_dt.day)

            self.assertEqual(0, new_dt.hour)
            self.assertEqual(0, new_dt.minute)
            self.assertEqual(0, new_dt.second)
            self.assertEqual(0, new_dt.microsecond)

        with self.subTest(name='get timestamp plus one day'):
            timestamp_plus_one_day = TimestampConverter.get_timestamp_plus_one_day(timestamp_with_zeroed_time)

            self.assertEqual(1571529600000, timestamp_plus_one_day)

            new_dt = TimestampConverter.get_datetime_from_timestamp(timestamp_plus_one_day)

            self.assertEqual(2019, new_dt.year)
            self.assertEqual(10, new_dt.month)
            self.assertEqual(20, new_dt.day)

            self.assertEqual(0, new_dt.hour)
            self.assertEqual(0, new_dt.minute)
            self.assertEqual(0, new_dt.second)
            self.assertEqual(0, new_dt.microsecond)


if __name__ == '__main__':
    unittest.main()
