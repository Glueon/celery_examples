from time import sleep, time
from celery import shared_task
import eventlet


def blocking_slow_io_operations():
    """Emulates some slow I/O operations like HTTP requests
    """
    print('Started doing slow operation')
    sleep(1)


def non_blocking_slow_io_operations():
    """Emulates some slow non-blocking I/O operations like HTTP requests
    """
    print('Started doing slow operation')
    eventlet.sleep(1)


@shared_task
def add_blocking(x, y):
    """
    Sample task which performs slow blocking I/O and then calculates and returns sum of 2 given numbers
    """
    blocking_slow_io_operations()
    return x + y


@shared_task
def add_non_blocking(x, y):
    """
    Sample task which executes slow non-blocking I/O and then calculates and returns sum of 2 given numbers
    """
    non_blocking_slow_io_operations()
    return x + y


@shared_task
def parser_with_speed_control(number_of_requests, execution_time, url):
    """Emulates a parser which given an API URL tries to make given number of requests in a given time.
       Usually API has some rate limit. Using number_of_requests and execution_time param user gives a clue what is maximum of requests/second is.
       So script tries to work not faster than the number_of_requests/execution_time but can work slower if there is a huge latency or problems with the API. Usually that is acceptable.
    """
    seconds_per_request = execution_time / number_of_requests

    for i in range(number_of_requests):
        print('{}. {}/{}'.format(url, i, number_of_requests + 1))
        start = time()
        # Emulate some network I/O like GET/POST requests, etc
        non_blocking_slow_io_operations()

        # See how long did it take to do all the needed operations
        elapsed = time() - start

        if elapsed < seconds_per_request:
            freeze_time = seconds_per_request - elapsed
            print('Elapsed {}. Freezing for {}'.format(elapsed, freeze_time))
            eventlet.sleep(freeze_time)

        print('Done')
