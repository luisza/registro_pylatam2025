# encoding: utf-8

'''
Free as freedom will be 27/10/2016

@author: luisza
'''

from __future__ import unicode_literals
from proposal import views
from django.urls import path

app_name = 'proposal'
urlpatterns = [
    path('', views.SpeechListView.as_view(), name='speech-list'),
    path('create/', views.createUpdateview, name='create'),
    path('<int:speech_id>/update/', views.createUpdateview, name='update'),
    path('<int:speech_id>/delete/', views.deleteView, name='delete'),
]