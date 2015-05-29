from celery import Celery
from tasks import add_non_blocking
from celery import group


app = Celery(__file__)
app.config_from_object('celeryconfig')

# Create a signature of a function. Think of it as an alias for further easier usage
one_plus_one_task = add_non_blocking.s(1, 1)

# Create 6 one_plus_one_task tasks which will run all in parallel in a single thread.
group(one_plus_one_task for _ in range(6)).delay()

"""
As soon as we hit hit the eventlet.sleep(...) in the non_blocking_slow_io_operations(...) celery will run another task from the group. This can be seen in the Celery output:

    [2015-05-29 18:58:54,021: INFO/MainProcess] Received task: tasks.add_non_blocking[2287c782-c048-419f-a653-6aea63b61e97]
    [2015-05-29 18:58:54,024: WARNING/MainProcess] Started doing slow operation
    [2015-05-29 18:58:54,024: INFO/MainProcess] Received task: tasks.add_non_blocking[6a0a5515-df02-4cf4-a4d2-170f43f93e60]
    [2015-05-29 18:58:54,026: WARNING/MainProcess] Started doing slow operation
    [2015-05-29 18:58:54,027: INFO/MainProcess] Received task: tasks.add_non_blocking[a354d51e-36f7-4f3a-b504-bb893e72e7fd]
    [2015-05-29 18:58:54,029: WARNING/MainProcess] Started doing slow operation
    [2015-05-29 18:58:54,029: INFO/MainProcess] Received task: tasks.add_non_blocking[e048e681-7cd2-48d2-a5bf-da2fdf857bcb]
    [2015-05-29 18:58:54,032: WARNING/MainProcess] Started doing slow operation
    [2015-05-29 18:58:54,032: INFO/MainProcess] Received task: tasks.add_non_blocking[0692029f-2f02-4f3b-9349-e55205abcd79]
    [2015-05-29 18:58:54,034: WARNING/MainProcess] Started doing slow operation
    [2015-05-29 18:58:54,035: INFO/MainProcess] Received task: tasks.add_non_blocking[720a14dd-41ca-460e-8424-a1341e68adf4]
    [2015-05-29 18:58:54,036: WARNING/MainProcess] Started doing slow operation
    [2015-05-29 18:58:55,027: INFO/MainProcess] Task tasks.add_non_blocking[2287c782-c048-419f-a653-6aea63b61e97] succeeded in 1.0043010350782424s: 2
    [2015-05-29 18:58:55,028: INFO/MainProcess] Task tasks.add_non_blocking[6a0a5515-df02-4cf4-a4d2-170f43f93e60] succeeded in 1.0027076558908448s: 2
    [2015-05-29 18:58:55,031: INFO/MainProcess] Task tasks.add_non_blocking[a354d51e-36f7-4f3a-b504-bb893e72e7fd] succeeded in 1.0032784020295367s: 2
    [2015-05-29 18:58:55,033: INFO/MainProcess] Task tasks.add_non_blocking[e048e681-7cd2-48d2-a5bf-da2fdf857bcb] succeeded in 1.0028874489944428s: 2
    [2015-05-29 18:58:55,036: INFO/MainProcess] Task tasks.add_non_blocking[0692029f-2f02-4f3b-9349-e55205abcd79] succeeded in 1.003232431015931s: 2
    [2015-05-29 18:58:55,038: INFO/MainProcess] Task tasks.add_non_blocking[720a14dd-41ca-460e-8424-a1341e68adf4] succeeded in 1.0027594560524449s: 2

After 'Started doing slow operation' immediately there is a new task received. So eventually we'll end up with 6 running tasks all waiting for 1 second. This is why takes only 1 second."""
