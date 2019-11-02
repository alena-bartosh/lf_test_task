import numpy as np
from timestamp_converter import TimestampConverter


class QueryStatisticCalculator:
    """Class for calculating statistics from the received queries dataframe
    """
    EXPECTED_COLUMNS = {
        'query_id': np.dtype('int64'),
        'status': np.dtype('int64'),
        'time': np.dtype('int64'),
        'rows': np.dtype('int64'),
        'threads': np.dtype('object')
    }

    def __init__(self, queries_df):
        """
        Args:
            queries_df (pandas.DataFrame): queries dataframe with such data:
            'query_id', 'status', 'time', 'rows', 'threads'.
        Raises:
            ValueError: if not received expected column names
            ValueError: if not received expected column types
        """
        if not np.all(queries_df.columns.values == [*QueryStatisticCalculator.EXPECTED_COLUMNS]):
            raise ValueError(f'Expected column names "{[*QueryStatisticCalculator.EXPECTED_COLUMNS]}" '
                             f'but "{queries_df.columns.values}" are given')

        if not np.all(queries_df.dtypes.values == [*QueryStatisticCalculator.EXPECTED_COLUMNS.values()]):
            raise ValueError(f'Expected column types "{[*QueryStatisticCalculator.EXPECTED_COLUMNS.values()]}" '
                             f'but "{queries_df.dtypes.values}" are given')

        df_merged_queries = queries_df.loc[queries_df['status'] == 0] \
            .drop(['status', 'rows', 'threads'], axis=1) \
            .rename(columns={'time': 'start'}) \
            .merge(queries_df.loc[queries_df['status'] == 1]
                   .drop(['status'], axis=1)
                   .rename(columns={'time': 'finish'}))

        self.df_queries = df_merged_queries
        self.min_timestamp = df_merged_queries.start.min()
        self.max_timestamp = df_merged_queries.finish.max()

    def check_timestamp_in_df(self, timestamp):
        """Сhecks if datetime is contained in the queries dataframe

        Args:
            timestamp (int): date in epoch millisecond format
        Raises:
            ValueError: If ``timestamp`` is less or more than existing in dateframe
        """
        if self.min_timestamp > timestamp or self.max_timestamp < timestamp:
            raise ValueError(f'Timestamp "{timestamp}" should be in the range '
                             f'["{self.min_timestamp}","{self.max_timestamp}"]')

    def check_timestamps_in_df(self, start_timestamp, finish_timestamp):
        """Сhecks if time range are contained in the queries dataframe, and they are entered correctly

        Args:
            start_timestamp (int): start datetime in epoch millisecond format
            finish_timestamp (int): finish datetime in epoch millisecond format
        Raises:
            ValueError: If ``start_timestamp`` and ``finish_timestamp`` is equal
            ValueError: If ``start_timestamp`` less than ``finish_timestamp`` is equal
        """
        self.check_timestamp_in_df(start_timestamp)
        self.check_timestamp_in_df(finish_timestamp)

        if start_timestamp == finish_timestamp:
            raise ValueError(f'Start timestamp and finish timestamp should be not equal. '
                             f'The current value is "{start_timestamp}"')

        if start_timestamp > finish_timestamp:
            raise ValueError(f'Start timestamp "{start_timestamp}" '
                             f'should be less than finish timestamp "{finish_timestamp}"')

    def get_average_elapsed_seconds_on_date(self, timestamp):
        """Gets average elapsed time for all queries on certain date

        Args:
            timestamp (int): date in epoch millisecond format
        Returns:
            float: average elapsed time in seconds
        """
        self.check_timestamp_in_df(timestamp)

        start_date_timestamp = TimestampConverter.get_timestamp_with_zeroed_time(timestamp)
        next_date_timestamp = TimestampConverter.get_timestamp_plus_one_day(start_date_timestamp)

        queries_by_day = self.df_queries.loc[(self.df_queries['start'] >= start_date_timestamp) &
                                             (self.df_queries['finish'] < next_date_timestamp)]

        return (queries_by_day.finish - queries_by_day.start).mean() / TimestampConverter.MILLISECONDS_PER_SECOND

    def get_average_row_count(self, start_timestamp, finish_timestamp):
        """Gets average per second number of rows returned from all queries during certain time range

        Args:
            start_timestamp (int): start datetime in epoch millisecond format
            finish_timestamp (int): finish datetime in epoch millisecond format
        Returns:
            float: average per second number of rows
        """
        self.check_timestamps_in_df(start_timestamp, finish_timestamp)

        queries_in_range = self.df_queries.loc[(self.df_queries['start'] >= start_timestamp) &
                                               (self.df_queries['finish'] <= finish_timestamp)]
        elapsed_time = (finish_timestamp - start_timestamp) / TimestampConverter.MILLISECONDS_PER_SECOND

        return queries_in_range.rows.sum() / elapsed_time

    def get_average_row_count_per_thread(self, start_timestamp, finish_timestamp):
        """Gets average per thread number of rows returned from all queries during certain time range

        Args:
            start_timestamp (int): start datetime in epoch millisecond format
            finish_timestamp (int): finish datetime in epoch millisecond format
        Returns:
            float: average per thread number of rows
        """
        self.check_timestamps_in_df(start_timestamp, finish_timestamp)

        queries_in_range = self.df_queries.loc[(self.df_queries['start'] >= start_timestamp) &
                                               (self.df_queries['finish'] <= finish_timestamp)]
        threads = set()

        for threads_as_str in queries_in_range.threads:
            threads.update(threads_as_str.split(','))

        if not threads:
            return 0

        return queries_in_range.rows.sum() / len(threads)

    def get_average_thread_per_second(self, start_timestamp, finish_timestamp):
        """Gets average per second number of threads executing at the same time during certain time range

        Args:
            start_timestamp (int): start datetime in epoch millisecond format
            finish_timestamp (int): finish datetime in epoch millisecond format
        Returns:
            float: average per second number of threads
        """
        self.check_timestamps_in_df(start_timestamp, finish_timestamp)

        queries_in_range = self.df_queries.loc[(self.df_queries['start'] >= start_timestamp) &
                                               (self.df_queries['finish'] <= finish_timestamp)]

        threads_count_column = queries_in_range.apply(lambda row: len(row.threads.split(',')), axis=1)
        elapsed_time = (finish_timestamp - start_timestamp)

        return ((queries_in_range.finish - queries_in_range.start) * threads_count_column).sum() / elapsed_time \
               / TimestampConverter.MILLISECONDS_PER_SECOND
