from django_rq import job


def task(*args, **kwargs):
    print('Hi!')
