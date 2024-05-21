from . import views
from django.urls import path, include


urlpatterns = [
    path('', views.index, name='home'),
    path('one-rep-maximum/', views.one_rep_maximum, name='one-rep-maximum')
]
