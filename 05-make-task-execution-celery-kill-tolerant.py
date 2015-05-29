from celery import Celery
from tasks import task_which_reruns_if_celery_is_killed


app = Celery(__file__)
app.config_from_object('celeryconfig')

task_which_reruns_if_celery_is_killed(200, 'http://hello_worl.com').delay()
