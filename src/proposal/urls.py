# encoding: utf-8

'''
Free as freedom will be 27/10/2016

@author: luisza
'''

from __future__ import unicode_literals

from rest_framework.routers import DefaultRouter

from proposal import views, types, topics, special_activities, rooms
from django.urls import path, include

from proposal.views import EventScheduleViewSet

router = DefaultRouter()
router.register(r'schedule/events', EventScheduleViewSet, basename='events')

app_name = 'proposal'
urlpatterns = [
    path('', views.SpeechListView.as_view(), name='speech-list'),
    path('create/', views.createUpdateview, name='create'),
    path('<int:speech_id>/update/', views.createUpdateview, name='update'),
    path('<int:speech_id>/delete/', views.deleteView, name='delete'),
    path('createTopic/', topics.CreateTopic.as_view(), name='create-topic'),
    path('createType/', types.CreateType.as_view(), name='create-type'),
    path('createRoom/', rooms.CreateRoom.as_view(), name='create-room'),
    path('filterSpeeches/', views.get_all_speeches, name='filter-speeches'),
    path('createSpecial/', special_activities.CreateSpecialActivity.as_view(), name='create-special'),
    path('schedule/events/delete-events/', views.removeSpeechScheduleFromCalendarView, name='delete-events'),
]

urlpatterns += router.urls
