from django.urls import include, path
from django.contrib import admin


urlpatterns = []

urlpatterns += [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('check/', include('check.urls')),
]