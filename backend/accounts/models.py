from django.db import models

# Create your models here.
class Contact(models.Model):
    """
    Represents a contact in the system.

    Attributes:
        name (str): The name of the contact.
        email (str): The email address of the contact.
        phone (str): The phone number of the contact.
        owner (User): The owner of the contact.
        created_at (datetime): The date and time when the contact was created.
        updated_at (datetime): The date and time when the contact was last updated.
    """

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    owner = models.ForeignKey('auth.User', related_name='contacts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
