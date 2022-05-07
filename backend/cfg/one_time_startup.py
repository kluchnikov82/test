import django_rq
# from .tasks import task
from redis import Redis
from datetime import timedelta, datetime
from rq_scheduler import Scheduler
from rq import Queue, Worker


def task(*args, **kwargs):
    print('Hi!')


def clear_add_task():
    scheduler = django_rq.get_scheduler('default')
    for job in scheduler.get_jobs():
        job.delete()

    redis_conn = Redis()
    scheduler = Scheduler(connection=redis_conn)
    scheduler.schedule(datetime.utcnow(), task, interval=1)
