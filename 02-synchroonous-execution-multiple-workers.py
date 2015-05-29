from celery import Celery
from tasks import add_blocking
from celery import group


app = Celery(__file__)
app.config_from_object('celeryconfig')
app.conf.update(CELERYD_CONCURRENCY=2)

# Create a signature of a function. Think of it as an alias for further easier usage
one_plus_one_task = add_blocking.s(1, 1)

"""
Create 6 one_plus_one_task tasks which will run 3 tasks in parallel because CELERYD_CONCURRENCY is 2
So it will take about 2 seconds
"""

group(one_plus_one_task for _ in range(6)).delay()

"""You'll see something like:
[2015-05-29 18:50:04,105: INFO/MainProcess] Task tasks.add_blocking[5bb9af46-2238-45ee-bd8e-b507f063ff08] succeeded in 1.0041172810597345s: 2
[2015-05-29 18:50:04,107: INFO/MainProcess] Task tasks.add_blocking[75cca160-71a6-4633-b851-a486f32e84f6] succeeded in 1.0034233749611303s: 2
[2015-05-29 18:50:05,108: INFO/MainProcess] Task tasks.add_blocking[521d884c-2559-4785-bba6-cdb364f3eda1] succeeded in 1.0024645259836689s: 2
[2015-05-29 18:50:05,110: INFO/MainProcess] Task tasks.add_blocking[b80d0d5e-377b-47fa-aebd-f9dd27b3899f] succeeded in 1.0022636549547315s: 2
[2015-05-29 18:50:06,111: INFO/MainProcess] Task tasks.add_blocking[f165c0a9-68ee-42a4-9d90-182b652a383c] succeeded in 1.0023803879739717s: 2
[2015-05-29 18:50:06,113: INFO/MainProcess] Task tasks.add_blocking[bf4abf83-c1aa-4a2f-8bcb-1de5b1bf7bfe] succeeded in 1.0021864490117878s: 2
"""
