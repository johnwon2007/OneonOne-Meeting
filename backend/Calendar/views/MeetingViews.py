# meetings/views.py

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, \
    DestroyAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from ..permissions import IsOwnerOrReadOnly
from ..models.meeting import Meeting
from ..serializers.meeting_serializer import MeetingCreateSerializer, \
    MeetingUpdateSerializer, MeetingCalendarViewSerializer
from ..models.calendar import Calendar
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import AllowAny
from ..services import SuggestionTimes, SendEmail, SendNotification


class MeetingCreateView(CreateAPIView):
    """
    View for creating a new meeting.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MeetingCreateSerializer

    def perform_create(self, serializer):
        """
        Custom logic for creating a meeting, such as setting the meeting's creator.
        """
        calendar_id = self.kwargs.get('calendar_id')
        print(calendar_id)
        try:
            calendar = Calendar.objects.get(pk=calendar_id)
        except Calendar.DoesNotExist:
            raise NotFound(detail="Calendar not found.")
        meeting = serializer.save(calendar=calendar)
        inviter = calendar.creator.first_name + " " + calendar.creator.last_name if calendar.creator.first_name + calendar.creator.last_name != "" else calendar.creator.email
        meeting_title = calendar.title
        url = meeting.url
        print([meeting.receiver_email, inviter, meeting_title, url])
        # Now sending the email
        SendEmail(meeting.receiver_email, inviter, meeting_title, url)


class MeetingDetailsView(RetrieveAPIView):
    """
    View for retrieving the details of a specific meeting.
    """
    permission_classes = [AllowAny]
    queryset = Meeting.objects.all()
    serializer_class = MeetingCalendarViewSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'meeting_id'


class MeetingUpdateView(UpdateAPIView):
    """
    View for updating the details of a specific meeting.
    """
    permission_classes = [AllowAny]
    queryset = Meeting.objects.all()
    serializer_class = MeetingUpdateSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'meeting_id'


class MeetingsView(ListAPIView):
    """
    View for listing all meetings associated with the authenticated user.
    """
    permission_classes = [AllowAny]
    serializer_class = MeetingCalendarViewSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Only return meetings for the currently authenticated user.
        """
        user = self.request.user
        return Meeting.objects.filter(receiver=user)


class MeetingDeleteView(DestroyAPIView):
    """
    View for deleting a specific meeting.
    """
    queryset = Meeting.objects.all()
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'id'
    lookup_url_kwarg = 'meeting_id'


class MeetingTimeSuggestionView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        calendar_id = self.kwargs.get('calendar_id')
        meeting_id = self.kwargs.get('meeting_id')

        try:
            calendar = Calendar.objects.get(pk=calendar_id)
        except Calendar.DoesNotExist:
            return Response({'error': 'Calendar not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        try:
            meeting = Meeting.objects.get(pk=meeting_id, calendar=calendar)
        except Meeting.DoesNotExist:
            return Response(
                {'error': 'Meeting not found in the specified calendar.'},
                status=status.HTTP_404_NOT_FOUND)
        best_time = SuggestionTimes(
            # Assuming your function needs these parameters
            calendar_availabilities=calendar.availability_calendar.all(),
            meeting_availabilities=meeting.availability_meeting.all(),
            meeting_duration=meeting.calendar.duration  # Example parameter
        )

        if best_time:
            return Response(best_time, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Could not find a suitable meeting time.'},
                status=status.HTTP_404_NOT_FOUND)


class MeetingNotifyView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        calendar_id = self.kwargs.get('calendar_id')
        meeting_id = self.kwargs.get('meeting_id')
        try:
            calendar = Calendar.objects.get(id=calendar_id)
            meeting = Meeting.objects.get(id=meeting_id, calendar=calendar)
            email_to = meeting.receiver_email
            inviter = calendar.creator.first_name + " " + calendar.creator.last_name if calendar.creator.first_name + calendar.creator.last_name != "" else calendar.creator.email
            meeting_title = calendar.title
            url = meeting.url

            SendNotification(email_to=email_to, inviter=inviter,
                             meeting_title=meeting_title, url=url)
            return Response({"message": "Notification sent successfully."},
                            status=status.HTTP_200_OK)
        except Calendar.DoesNotExist:
            return Response({"error": "Calendar not found."},
                            status=status.HTTP_404_NOT_FOUND)
        except Meeting.DoesNotExist:
            return Response({"error": "Meeting not found."},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
