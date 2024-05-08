from django.db import models


class Calendar(models.Model):
    """
    Represents a calendar object.

    Attributes:
        title (str): The title of the calendar.
        description (str): The description of the calendar.
        location (str): The location of the calendar.
        duration (int): The duration of the calendar.
        creator (User): The creator of the calendar.
    """

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    duration = models.IntegerField()
    creator = models.ForeignKey('auth.User', related_name='user', on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns a string representation of the calendar.

        Returns:
            str: The title of the calendar.
        """
        return self.title
