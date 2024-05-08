from django.db import models

class Availability(models.Model):
    """
    Represents the availability of a calendar at a specific date and time.

    Attributes:
        date_time (DateTimeField): The date and time of the availability.
        calendar (ForeignKey): The associated calendar for this availability.
        preference (IntegerField): The preference level for this availability.
    """

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    calendar = models.ForeignKey('Calendar', related_name='availability_calendar', on_delete=models.CASCADE)
    preference = models.IntegerField()

    def __str__(self):
        return f'{self.start_time} ~ {self.end_time}'
