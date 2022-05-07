from django.urls import include, path
from django.contrib import admin
from .one_time_startup import clear_add_task


urlpatterns = []

urlpatterns += [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('check/', include('check.urls')),
]

urlpatterns += [
    path('django-rq/', include('django_rq.urls'))
]

clear_add_task()