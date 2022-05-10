from django.urls import include, path
import check.views as views

urlpatterns = []

urlpatterns += [
    path('create_checks/', views.CreateChecksView.as_view(), name='create-checks'),
    path('new_checks/', views.NewChecksView.as_view(), name='new-checks'),
    path('check/', views.CheckView.as_view(), name='check'),
]