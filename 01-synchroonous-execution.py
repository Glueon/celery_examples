from celery import Celery
from tasks import add_blocking
from celery import group


app = Celery(__file__)
app.config_from_object('celeryconfig')
app.conf.update(CELERYD_CONCURRENCY=1)

# Create a signature of a function. Think of it as an alias for further easier usage
one_plus_one_task = add_blocking.s(1, 1)

# Create 6 one_plus_one_task tasks which will run sequentially because we started celery with one worker thread (CELERYD_CONCURRENCY=1)
# It will take about 6 seconds to run
group(one_plus_one_task for _ in range(6)).delay()
