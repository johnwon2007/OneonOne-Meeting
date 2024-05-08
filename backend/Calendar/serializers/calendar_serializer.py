from rest_framework import serializers
from ..models.calendar import Calendar
from ..models.availability import Availability
from .availability_serializer import AvailabilityCreateSerializer, \
    AvailabilityViewSerializer, AvailabilityUpdateSerializer


class CalendarCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new calendar.

    This serializer is used to create a new calendar object with its associated availability objects.

    Attributes:
        availability_calendar (AvailabilityCreateSerializer): Serializer for creating availability objects.

    """

    availability_calendar = AvailabilityCreateSerializer(many=True)

    class Meta:
        model = Calendar
        fields = ["title", "description", "duration", "location",
                  "availability_calendar"]

    def create(self, validated_data):
        """
        Create a new calendar object.

        This method creates a new calendar object with the provided validated data.
        It also creates the associated availability objects.

        Args:
            validated_data (dict): The validated data for creating the calendar.

        Returns:
            Calendar: The created calendar object.

        """
        availability_data = validated_data.pop("availability_calendar")
        calendar = Calendar.objects.create(**validated_data)
        for availability in availability_data:
            Availability.objects.create(calendar=calendar, **availability)
        return calendar


# Serializer for only calendars (No meetings)
class CalendarViewSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing a calendar.

    This serializer is used to view the details of a calendar object with its associated availability objects.

    Attributes:
        availability_calendar (AvailabilityViewSerializer): Serializer for viewing availability objects.

    """

    availability_calendar = AvailabilityViewSerializer(many=True)

    class Meta:
        model = Calendar
        fields = ["id", "title", "description", "duration", "location",
                  "availability_calendar", 'creator']
        extra_kwargs = {'id': {'read_only': True}}


# serializer for calendar and its all meetings.
class CalendarMeetingViewSerializer(serializers.ModelSerializer):
    from .meeting_serializer import MeetingViewSerializer
    """
    Serializer for viewing a calendar.

    This serializer is used to view the details of a calendar object with its associated availability objects.

    Attributes:
        availability_calendar (AvailabilityViewSerializer): Serializer for viewing availability objects.

    """

    availability_calendar = AvailabilityViewSerializer(many=True,
                                                       read_only=True)
    meeting = MeetingViewSerializer(many=True, read_only=True)
    class Meta:
        model = Calendar
        fields = ["id", "title", "description", "duration", "location",
                  "availability_calendar", 'creator', "meeting"]
        extra_kwargs = {'id': {'read_only': True}}


class CalendarUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a calendar.

    This serializer is used to update the details of a calendar object.
    It also updates the associated availability objects.

    Attributes:
        availability_calendar (AvailabilityUpdateSerializer): Serializer for updating availability objects.

    """

    availability_calendar = AvailabilityUpdateSerializer(many=True)

    class Meta:
        model = Calendar
        fields = ['id', 'title', 'description', 'duration', "location",
                  'availability_calendar']

    def update(self, instance, validated_data):
        """
        Update a calendar object.

        This method updates the details of a calendar object with the provided validated data.
        It also updates the associated availability objects.

        Args:
            instance (Calendar): The calendar object to be updated.
            validated_data (dict): The validated data for updating the calendar.

        Returns:
            Calendar: The updated calendar object.

        """
        availabilities_data = validated_data.pop('availability_calendar', [])
        instance = super().update(instance, validated_data)

        current_availability_ids = set(
            instance.availability_calendar.values_list('id', flat=True))
        updated_availability_ids = set()
        print(current_availability_ids)

        for availability_data in availabilities_data:
            availability_id = availability_data.get('id', None)
            # if 'id' in the current database update it:
            if availability_id in current_availability_ids:
                avail_instance = Availability.objects.get(id=availability_id)
                for key, value in availability_data.items():
                    setattr(avail_instance, key, value)
                avail_instance.save()
                updated_availability_ids.add(availability_id)
            # if id does not exists (we should give new availability id value of or None but it might raise is_valid error -1)
            else:
                availability_data['id'] = None
                new_availability = Availability.objects.create(
                    calendar=instance, **availability_data)
                updated_availability_ids.add(new_availability.id)
        availabilities_to_delete = current_availability_ids - updated_availability_ids
        # after updating any changes remove deleted fields
        if availabilities_to_delete:
            Availability.objects.filter(
                id__in=availabilities_to_delete).delete()

        return instance
