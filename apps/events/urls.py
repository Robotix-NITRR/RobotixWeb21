from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('',views.event_api,name='event_api')
]