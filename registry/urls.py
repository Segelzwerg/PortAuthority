from django.urls import path
from . import views

app_name = 'registry'

urlpatterns = [
    path('', views.ApplicationListView.as_view(), name='application_list'),
    path('applications/', views.ApplicationListView.as_view(), name='applications'),
]
