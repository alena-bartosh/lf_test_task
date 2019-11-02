import unittest
from sys import maxsize as really_big_number
import pandas as pd
from query_statistic_calculator import QueryStatisticCalculator


class QueryStatisticCalculatorTestCase(unittest.TestCase):
    START_TIMESTAMP_IN_TEST_DATA = 1571356830600
    FINISH_TIMESTAMP_IN_TEST_DATA = 1571356838845

    def test_raise_exception_when_incorrect_dataframe(self):
        with self.subTest(name='empty dataframe'):
            empty_df = pd.DataFrame()

            with self.assertRaises(ValueError):
                query_statistic_calculator = QueryStatisticCalculator(empty_df)

        with self.subTest(name='wrong column names in dataframe'):
            df_with_wrong_column_name = pd.DataFrame(data={'query_id_WRONG': 1,
                                                           'status': 2,
                                                           'time': 3,
                                                           'rows': 4,
                                                           'threads': ['5,6,7']})

            with self.assertRaises(ValueError):
                query_statistic_calculator = QueryStatisticCalculator(df_with_wrong_column_name)

        with self.subTest(name='wrong column types in dataframe'):
            df_with_wrong_column_types = pd.DataFrame(columns=['query_id', 'status', 'time', 'rows', 'threads'])

            with self.assertRaises(ValueError):
                query_statistic_calculator = QueryStatisticCalculator(df_with_wrong_column_types)

    def test_successful_creation_when_correct_dataframe(self):
        df = pd.DataFrame(data={'query_id': 1,
                                'status': 2,
                                'time': 3,
                                'rows': 4,
                                'threads': ['5,6,7']})

        query_statistic_calculator = QueryStatisticCalculator(df)

    def test_raise_exception_when_timestamp_not_in_dataframe(self):
        df = pd.read_csv('tests/queries_sample.tsv', sep='\t')

        query_statistic_calculator = QueryStatisticCalculator(df)

        with self.subTest(name='timestamp is less than minimal dataframe timestamp'):
            with self.assertRaises(ValueError):
                query_statistic_calculator.check_timestamp_in_df(1)

        with self.subTest(name='timestamp is more than minimal dataframe timestamp'):
            with self.assertRaises(ValueError):
                query_statistic_calculator.check_timestamp_in_df(really_big_number)

    def test_average_elapsed_time_is_calculated_correctly(self):
        df = pd.read_csv('tests/queries_sample.tsv', sep='\t')

        query_statistic_calculator = QueryStatisticCalculator(df)

        average_elapsed_time = query_statistic_calculator.get_average_elapsed_seconds_on_date(
            QueryStatisticCalculatorTestCase.START_TIMESTAMP_IN_TEST_DATA)
        self.assertAlmostEqual(3.04475, average_elapsed_time)

    def test_average_row_count_is_calculated_correctly(self):
        df = pd.read_csv('tests/queries_sample.tsv', sep='\t')

        query_statistic_calculator = QueryStatisticCalculator(df)

        average_row_count = query_statistic_calculator.get_average_row_count(
            QueryStatisticCalculatorTestCase.START_TIMESTAMP_IN_TEST_DATA,
            QueryStatisticCalculatorTestCase.FINISH_TIMESTAMP_IN_TEST_DATA)
        self.assertAlmostEqual(8.49, average_row_count, places=2)

    def test_average_row_count_per_thread_is_calculated_correctly(self):
        df = pd.read_csv('tests/queries_sample.tsv', sep='\t')

        query_statistic_calculator = QueryStatisticCalculator(df)

        average_row_count_per_thread = query_statistic_calculator.get_average_row_count_per_thread(
            QueryStatisticCalculatorTestCase.START_TIMESTAMP_IN_TEST_DATA,
            QueryStatisticCalculatorTestCase.FINISH_TIMESTAMP_IN_TEST_DATA)
        self.assertAlmostEqual(5, average_row_count_per_thread)

    def test_average_thread_per_second_is_calculated_correctly(self):
        df = pd.read_csv('tests/queries_sample.tsv', sep='\t')

        query_statistic_calculator = QueryStatisticCalculator(df)

        average_thread_per_second = query_statistic_calculator.get_average_thread_per_second(
            QueryStatisticCalculatorTestCase.START_TIMESTAMP_IN_TEST_DATA,
            QueryStatisticCalculatorTestCase.FINISH_TIMESTAMP_IN_TEST_DATA)
        self.assertAlmostEqual(0.0087, average_thread_per_second, places=4)


if __name__ == '__main__':
    unittest.main()
