from rest_framework import serializers
from ..models.meetingAvailability import MeetingAvailability

class MeetingAvailabilityCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating MeetingAvailability objects.

    Fields:
    - start_time: DateTimeField representing the start time of availability.
    - end_time: DateTimeField representing the end time of availability.
    - preference: IntegerField representing the preference level.

    Usage:
    - Use this serializer to create new MeetingAvailability objects.
    """
    class Meta:
        model = MeetingAvailability
        fields = ['start_time', 'end_time', 'preference']


class MeetingAvailabilityViewSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing MeetingAvailability objects.

    Fields:
    - id: IntegerField representing the unique identifier of the meeting availability.
    - start_time: DateTimeField representing the start time of availability.
    - end_time: DateTimeField representing the end time of availability.
    - preference: IntegerField representing the preference level.

    Usage:
    - Use this serializer to view existing MeetingAvailability objects.
    """
    class Meta:
        model = MeetingAvailability
        fields = ['id', 'start_time', 'end_time', 'preference']
        extra_kwargs = {'id': {'read_only': True}}


class MeetingAvailabilityUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating MeetingAvailability objects.

    Fields:
    - id: IntegerField representing the unique identifier of the meeting availability (optional).
    - start_time: DateTimeField representing the updated start time of availability.
    - end_time: DateTimeField representing the updated end time of availability.
    - preference: IntegerField representing the updated preference level.

    Usage:
    - Use this serializer to update existing MeetingAvailability objects.
    """
    id = serializers.IntegerField(required=False)
    class Meta:
        model = MeetingAvailability
        fields = ['id', 'start_time', 'end_time', 'preference']
