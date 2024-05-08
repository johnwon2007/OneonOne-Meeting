from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, \
    DestroyAPIView, UpdateAPIView

from ..permissions import IsOwnerOrReadOnly
from ..serializers.calendar_serializer import CalendarCreateSerializer, \
    CalendarUpdateSerializer, CalendarMeetingViewSerializer
from rest_framework.permissions import IsAuthenticated
from ..models.calendar import Calendar


class CalendarCreateView(CreateAPIView):
    """
    View for creating a new calendar.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CalendarCreateSerializer

    def perform_create(self, serializer):
        """
        Perform the creation of a new calendar.
        """
        serializer.save(creator=self.request.user)


class CalendarDetailsView(RetrieveAPIView):
    """
    A view for retrieving details of a calendar.

    This view allows anyone to view the details of a calendar by providing the calendar ID in the URL.

    Attributes:
        queryset (QuerySet): The queryset of Calendar objects to retrieve from.
        serializer_class (Serializer): The serializer class to use for serializing the retrieved calendar object.
        lookup_field (str): The field to use for looking up the calendar object.
        lookup_url_kwarg (str): The URL keyword argument to use for retrieving the calendar ID from the URL.
    """
    queryset = Calendar.objects.all()
    serializer_class = CalendarMeetingViewSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'calendar_id'


class CalendarUpdateView(UpdateAPIView):
    """
    A view for updating a calendar object.

    This view allows authenticated users to update a calendar object.
    Only the owner of the calendar object can perform the update.

    Attributes:
        queryset (QuerySet): The queryset of Calendar objects.
        serializer_class (Serializer): The serializer class for updating a calendar object.
        permission_classes (list): The list of permission classes for the view.
        lookup_field (str): The field to use for looking up the calendar object.
        lookup_url_kwarg (str): The URL keyword argument for the lookup field.
    """
    queryset = Calendar.objects.all()
    serializer_class = CalendarUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = "id"
    lookup_url_kwarg = 'calendar_id'


class CalendarsView(ListAPIView):
    """
    A view for retrieving calendars created by the authenticated user.
    """
    serializer_class = CalendarMeetingViewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns the queryset of calendars created by the authenticated user.
        """
        user = self.request.user
        return Calendar.objects.filter(creator=user)


class CalendarDeleteView(DestroyAPIView):
    """
    A view for deleting a calendar object.

    Inherits from DestroyAPIView which provides a DELETE method handler.
    Requires authentication and permission to delete the calendar object.
    The calendar object is identified by the 'id' field in the URL.

    Attributes:
        queryset (QuerySet): The queryset of Calendar objects.
        permission_classes (list): The list of permission classes required for the view.
        lookup_field (str): The field used to look up the calendar object.
        lookup_url_kwarg (str): The URL keyword argument used to retrieve the calendar ID.
    """
    queryset = Calendar.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'id'
    lookup_url_kwarg = 'calendar_id'
