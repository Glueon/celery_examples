from celery import Celery, group
from tasks import parser_with_speed_control


app = Celery(__file__)
app.config_from_object('celeryconfig')


# The desired number of requests we want to make to our imaginary API
number_of_requests = 5
"""The execution time is number of seconds in which we expect this to finish. Not faster, but longer is ok.
Usually API has some limit on limit=requests/second, so execution_time = number_of_requests / limit"""
execution_time = 10
"""
So was ask to run not faster than 5 / 10 = 0.5 r/s. One request each 2 seconds.
Inside a task we call non_blocking_slow_io_operations which has an explicit 1 second sleep emulating work.
Without any limits the method will just run 1 request per second. But our desired speed is 1 request per 2 seconds.
So method will sleep for 1 second each iteration
"""

# Let's access two API's in parallel. We are using eventlet not threads, so we can add as many URL's as we need and they all will run together
group(parser_with_speed_control.s(number_of_requests=number_of_requests, execution_time=execution_time, url=url) for url in ('http://someapi.com/api', 'http://anotherapi/api'))()
"""
Given all both task will run in parallel 10 seconds in sum. That is what we asked for with the execution_time = 10:
    [2015-05-29 20:07:57,028: INFO/MainProcess] Task tasks.parser_with_speed_control[af3dca6c-094a-48b5-9af8-0b3d17268215] succeeded in 10.010644793044776s: None
    [2015-05-29 20:07:57,029: INFO/MainProcess] Task tasks.parser_with_speed_control[d8faf702-99c1-44ce-8d9f-fe4b2d1ec569] succeeded in 10.0142403250793s: None
"""

# If ask to run 5 requests in 1 second where each request takes 1 second to run there will be no freezes and tasks will complete in 5 seconds
number_of_requests = 5
execution_time = 1
group(parser_with_speed_control.s(number_of_requests=number_of_requests, execution_time=execution_time, url=url) for url in ('http://someapi.com/api', 'http://anotherapi/api'))()
"""Output:
    [2015-05-29 20:39:24,043: INFO/MainProcess] Task tasks.parser_with_speed_control[4e44f4c8-2467-4fa7-a044-56ffe9e7f63e] succeeded in 5.0108281769789755s: None
    [2015-05-29 20:39:24,044: INFO/MainProcess] Task tasks.parser_with_speed_control[94a08b50-5577-4e16-85b6-efb10b90fbc7] succeeded in 5.009133392944932s: None
"""
