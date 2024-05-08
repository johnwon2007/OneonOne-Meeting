from django.urls import path
from .views.CalendarViews import CalendarCreateView, CalendarsView, \
    CalendarUpdateView, CalendarDetailsView, CalendarDeleteView

from .views.MeetingViews import MeetingCreateView, MeetingDetailsView, \
    MeetingUpdateView, MeetingDeleteView, MeetingTimeSuggestionView, MeetingsView, MeetingNotifyView

app_name = 'Calendar'
urlpatterns = [
    #USED when creating new calendar
    path('add/', CalendarCreateView.as_view(), name='calendar_add'),
    #USED when all calendars of the current user is needed
    path('all/', CalendarsView.as_view(), name='calendars_all'),
    #USED when editing calendar
    path('<int:calendar_id>/edit', CalendarUpdateView.as_view(),
         name='calendar_edit'),
    #USED to get details of a calendar
    path('<int:calendar_id>/details', CalendarDetailsView.as_view(),
         name='calender_detail'),
    #USED to delete a calendar
    path('<int:calendar_id>/delete', CalendarDeleteView.as_view(),
         name='calendar_delete'),

    #USED when people are invited to Calendar/Event
    path('<int:calendar_id>/meetings/add/',
         MeetingCreateView.as_view(), name='meeting_add'),
    #USED when meeting is deleted
    path('<int:calendar_id>/meetings/<int:meeting_id>/delete/',
         MeetingDeleteView.as_view(), name='meeting_delete'),
    #USED when detail of a meeting is needed
    path('<int:calendar_id>/meetings/<int:meeting_id>/details/',
         MeetingDetailsView.as_view(), name='meeting_details'),
    #USED when all meetings of the current user is needed
    path('meetings/all/', MeetingsView.as_view(), name="meetings_all"),
    #USED when meeting is need to be edited
    path('<int:calendar_id>/meetings/<int:meeting_id>/edit/',
         MeetingUpdateView.as_view(), name='meeting_edit'),
    #USED to view suggested times for calendar and meeting
    path('<int:calendar_id>/meetings/<int:meeting_id>/suggest-time/', MeetingTimeSuggestionView.as_view(), name='meeting-time-suggestion'),
    #USED to notify the user to book the meeting
    #POST
    path('<int:calendar_id>/meetings/<int:meeting_id>/notify/', MeetingNotifyView.as_view(), name='meeting_notify')
]
