from django.urls import path
from . import views

urlpatterns = [
    path('summarize/', views.summarize, name='summarize'),
    path('services/',views.services,name='services'),
    path('output/',views.output,name='output'),
    path('',views.index,name='index'),
    path('team/',views.team,name='team')
]
