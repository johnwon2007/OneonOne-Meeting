from rest_framework import serializers
from ..models.availability import Availability
from ..models.meetingAvailability import MeetingAvailability


class AvailabilityCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating Availability objects.

    Fields:
    - date_time: DateTimeField representing the date and time of availability.
    - preference: IntegerField representing the preference level.

    Usage:
    - Use this serializer to create new Availability objects.
    """
    class Meta:
        model = Availability
        fields = ['start_time', 'end_time', 'preference']


class AvailabilityViewSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing Availability objects.

    Fields:
    - id: IntegerField representing the unique identifier of the availability.
    - date_time: DateTimeField representing the date and time of availability.
    - preference: IntegerField representing the preference level.

    Usage:
    - Use this serializer to view existing Availability objects.
    """
    class Meta:
        model = Availability
        fields = ['id', 'start_time', 'end_time', 'preference']
        extra_kwargs = {'id': {'read_only': True}}


class AvailabilityUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating Availability objects.

    Fields:
    - id: IntegerField representing the unique identifier of the availability (optional).
    - date_time: DateTimeField representing the updated date and time of availability.
    - preference: IntegerField representing the updated preference level.

    Usage:
    - Use this serializer to update existing Availability objects.
    """
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Availability
        fields = ['id', 'start_time', 'end_time', 'preference']
