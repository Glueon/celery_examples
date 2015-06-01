## Little demos of Celery usage

### Non example files
* `celeryconfig.py` - default configuration of the Celery daemon I use across all examples
* `tasks.py` - celery tasks I invoke in all examples
* `docker-compose.yml` - used to spin up a container with the redis which is used as a broker and a result storage.

### Examples
* `01-synchroonous-execution.py` - execute a group of tasks with blocking I/O in one Celery worker 
* `02-synchroonous-execution-multiple-workers.py` - same as the previous example but with multiple workrs
* `03-async-execution-with-eventlet.py` - execute a group of tasks with eventlet option enabled in celery and with non-blocking I/O
* `04-dynamic-rate-limit.py` - performs two tasks in parallel. Each task has a `for` loop which tries to execute external function not faster than the given speed. It's usually is used when you have an API which has some requests/second limitations.
* `05-make-task-execution-celery-kill-tolerant.py` - simple example of how to rerun a task in case of celery death.
* `06-dynamic-rate-limit-using-chains.py` - another approach for the previous example. Here instead of creating one big task we divide it into subtasks. So each for iteration from the previous example is no a seperate task. Tasks are linked using callbacks so whenever the tasks completes it notifies the second one that it should start working, supplying the ammount of seconds it should wait before it starts the work.


### Running examples

First of all install `docker-compose`. After that:
* Build containers and start redis container: `docker-compose up`
* Run an example using `docker-compose run EXAMPLE_NAME`:

To run an example which does not use `eventlet` (like `01-synchroonous-execution`) just type:

	docker-compose run celery 01-synchroonous-execution

For running eventlet examples (like `03-async-execution-with-eventlet`) use:

	docker-compose run celery 03-async-execution-with-eventlet -P eventlet

We need to specify the `-P eventlet` in a command line and can't set this setting in code because the docs [say](https://celery.readthedocs.org/en/latest/configuration.html#celeryd-pool):

> Never use this option to select the eventlet or gevent pool. You must use the -P option instead, otherwise the monkey patching will happen too late and things will break in strange and silent ways.
