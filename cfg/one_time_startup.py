import os

import django_rq
# from .tasks import task
from redis import Redis
from datetime import timedelta, datetime
from rq_scheduler import Scheduler
from check.models import Check, Printer
from django.conf import settings
from django.template.loader import render_to_string
import pdfkit


def task(*args, **kwargs):
    settings.configure()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cfg.settings')
    checks = Check.objects.filter(status='Новый')
    for check in checks:
        context = {'check': check}
        content = render_to_string('base_client_check.html', context)
        with open(str(settings.BASE_DIR) + '/templates/template.html', 'w') as static_file:
            static_file.write(content)

        pdfkit.from_file(str(settings.BASE_DIR) + '/templates/template.html',
                         str(settings.BASE_DIR) + '/media/' + str(check.order['id']) + '_client.pdf')

        content = render_to_string('base_kitchen_check.html', context)
        with open(str(settings.BASE_DIR) + '/templates/template.html', 'w') as static_file:
            static_file.write(content)

        pdfkit.from_file(str(settings.BASE_DIR) + '/templates/template.html',
                         str(settings.BASE_DIR) + '/media/' + str(check.order['id']) + '_kitchen.pdf')


def clear_add_task():
    scheduler = django_rq.get_scheduler('default')
    for job in scheduler.get_jobs():
        job.delete()

    redis_conn = Redis('172.19.0.103')
    scheduler = Scheduler(connection=redis_conn)
    scheduler.schedule(datetime.utcnow(), task, interval=1)
