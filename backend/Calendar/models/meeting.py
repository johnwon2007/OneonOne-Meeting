from django.db import models


class Meeting(models.Model):
    """
    Represents a meeting in the calendar.

    Attributes:
        receiver (str): The receiver of the meeting.
        status (bool): The status of the meeting.
        start_time (datetime): The start time of the meeting.
        calendar (Calendar): The calendar to which the meeting belongs.
    """
    receiver = models.ForeignKey('auth.User', related_name='received_meeting',
                                 null=True, on_delete=models.CASCADE)
    receiver_email = models.EmailField()
    status = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True)
    url = models.CharField(max_length=200, null=True)
    calendar = models.ForeignKey('Calendar', related_name='meeting',
                                 on_delete=models.CASCADE)

    def __str__(self):
        return self.calendar.title
