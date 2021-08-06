from django.urls import path
from . import views

app_name = 'functionapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('regist', views.regist, name='regist'),
]