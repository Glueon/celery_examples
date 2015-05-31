from celery import Celery, chain
from tasks import parser_with_speed_control_using_chain, final_parser_task
from uuid import uuid4


app = Celery(__file__)
app.config_from_object('celeryconfig')


# The desired number of requests we want to make to our imaginary API
number_of_requests = 5
execution_time = 10
task_id = uuid4()

# First task to be executed. Passing explicityly freeze_time equals to 0
initial_func = parser_with_speed_control_using_chain.s(0, number_of_requests, execution_time, 'http://hellowolrd.com', task_id)
# The same as the previous one, but without the freeze_time param.
parse_func = parser_with_speed_control_using_chain.s(number_of_requests, execution_time, 'http://hellowolrd.com', task_id)
# Cleans the temp data like iteration counters and reports that task succeded
clean_up_func = final_parser_task.s(task_id=task_id)

tasks_chain = [initial_func] + [parse_func] * (number_of_requests - 1) + [clean_up_func]
chain(*tasks_chain)()
