from time import sleep
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
