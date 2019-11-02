from flask import Flask, Response, request, abort, render_template
from functools import wraps
import pandas as pd
from query_statistic_calculator import QueryStatisticCalculator
from timestamp_converter import TimestampConverter


app = Flask(__name__)

df_queries = pd.read_csv('queries.tsv', sep='\t')
query_statistic_calculator = QueryStatisticCalculator(df_queries)


def get_int_value_from_get_parameter(param_name):
    timestamp_with_milliseconds = request.args.get(param_name)

    if timestamp_with_milliseconds is None:
        abort(Response(f'Error! "{param_name}" GET argument is required', status=400))

    return int(timestamp_with_milliseconds)


def handle_value_error(f):
    """Decorator to catch exceptions in inner function """
    @wraps(f)  # returns decorator with name of f(). it is needed to correct Flask endpoint registration
    def decorator():
        try:
            return f()
        except ValueError as e:
            app.logger.error(f'[{e}] during [{request}] processing')

            abort(Response(f'Error! Wrong input. Exception message: [{e}]', status=400))

    return decorator


@app.route('/')
@handle_value_error
def index():
    return render_template('index.html')


@app.route('/elapsed_time')
@handle_value_error
def elapsed_time():
    timestamp = get_int_value_from_get_parameter('timestamp')

    average_elapsed_time = query_statistic_calculator.get_average_elapsed_seconds_on_date(timestamp)
    dt = TimestampConverter.get_datetime_from_timestamp(timestamp)

    return f'The average elapsed time for all queries on {timestamp} ({dt:%d.%m.%Y}) ' \
           f'is {average_elapsed_time:.3f} seconds'


@app.route('/rows_per_second')
@handle_value_error
def number_of_rows_per_second():
    start_timestamp = get_int_value_from_get_parameter('start_timestamp')
    finish_timestamp = get_int_value_from_get_parameter('finish_timestamp')

    average_rows_per_second = query_statistic_calculator.get_average_row_count(start_timestamp, finish_timestamp)
    dt_start = TimestampConverter.get_datetime_from_timestamp(start_timestamp)
    dt_finish = TimestampConverter.get_datetime_from_timestamp(finish_timestamp)

    return f'The average per second number of rows returned from all queries ' \
           f'during {start_timestamp} ({dt_start}) and {finish_timestamp} ({dt_finish}) ' \
           f'is {average_rows_per_second:.3f}'


@app.route('/rows_per_thread')
@handle_value_error
def number_of_rows_per_thread():
    start_timestamp = get_int_value_from_get_parameter('start_timestamp')
    finish_timestamp = get_int_value_from_get_parameter('finish_timestamp')

    average_rows_per_thread = query_statistic_calculator.get_average_row_count_per_thread(start_timestamp,
                                                                                          finish_timestamp)
    dt_start = TimestampConverter.get_datetime_from_timestamp(start_timestamp)
    dt_finish = TimestampConverter.get_datetime_from_timestamp(finish_timestamp)

    return f'The average per thread number of rows returned from all queries ' \
           f'during {start_timestamp} ({dt_start}) and {finish_timestamp} ({dt_finish}) ' \
           f'is {average_rows_per_thread:.3f}'


@app.route('/thread_per_second')
@handle_value_error
def number_of_thread_per_second():
    start_timestamp = get_int_value_from_get_parameter('start_timestamp')
    finish_timestamp = get_int_value_from_get_parameter('finish_timestamp')

    average_thread_per_second = query_statistic_calculator.get_average_thread_per_second(start_timestamp,
                                                                                         finish_timestamp)
    dt_start = TimestampConverter.get_datetime_from_timestamp(start_timestamp)
    dt_finish = TimestampConverter.get_datetime_from_timestamp(finish_timestamp)

    return f'The average per second number of threads executing at the same ' \
           f'during {start_timestamp} ({dt_start}) and {finish_timestamp} ({dt_finish}) ' \
           f'is {average_thread_per_second:.3f}'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
