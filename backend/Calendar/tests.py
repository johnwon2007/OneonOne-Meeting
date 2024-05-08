from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models.calendar import Calendar
from .models.meeting import Meeting
from datetime import datetime

class MeetingViewTests(TestCase):
    def setUp(self):
        # Create a user and a client
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Create a calendar and a meeting
        self.calendar = Calendar.objects.create(title='Test Calendar', duration=30, creator=self.user)
        self.meeting = Meeting.objects.create(
            title='Test Meeting', receiver='test@example.com',
            status=False, start_time=datetime.now(), calendar=self.calendar
        )

    def test_add_meeting(self): ####
        url = reverse('Calendar:meeting_add', kwargs={'calendar_id': self.calendar.id})
        data = {
            'title': 'Team Meeting',
            'receiver': 'team@example.com',
            'status': False,
            'start_time': datetime.now()
        }
        response = self.client.post(url, data)
        print(response.data) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Meeting.objects.count(), 2)
        self.assertEqual(Meeting.objects.last().title, 'Team Meeting') ###

    def test_retrieve_meeting_details(self):
        url = reverse('Calendar:meeting_details', kwargs={'calendar_id': self.calendar.id, 'meeting_id': self.meeting.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.meeting.title)

    def test_update_meeting(self):
        url = reverse('Calendar:meeting_edit', kwargs={'calendar_id': self.calendar.id, 'meeting_id': self.meeting.id})
        new_time = datetime.now()
        data = {
            'title': 'Updated Meeting',
            'receiver': 'update@example.com',
            'status': True,
            'start_time': new_time
        }
        response = self.client.put(url, data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.meeting.refresh_from_db()
        self.assertEqual(self.meeting.title, 'Updated Meeting')
        self.assertEqual(self.meeting.receiver, 'update@example.com')

    def test_delete_meeting(self):
        url = reverse('Calendar:meeting_delete', kwargs={'calendar_id': self.calendar.id, 'meeting_id': self.meeting.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Meeting.DoesNotExist):
            Meeting.objects.get(id=self.meeting.id)

    def test_list_meetings(self):
        Meeting.objects.create(title='Team Meeting', receiver='team@example.com', calendar=self.calendar)
        url = reverse('Calendar:meetings_all', kwargs={'calendar_id': self.calendar.id})
        self.client.force_authenticate(user=self.user)  # Authenticating the user for the test client.
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('Team Meeting' in [m['title'] for m in response.data])

    def test_add_meeting_non_existent_calendar(self):
        url = reverse('Calendar:meeting_add', kwargs={'calendar_id': 9999})  # assuming 9999 is a non-existent calendar id
        data = {
            'title': 'Non-existent Calendar Meeting',
            'receiver': 'test@example.com',
            'status': False,
            'start_time': datetime.now().isoformat()
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_meeting_not_owned_by_user(self):########
        # Create another user and calendar only if it doesn't exist
        username = 'otheruser'
        if not User.objects.filter(username=username).exists():
            other_user = User.objects.create_user(username=username, password='testpassword')
        else:
            other_user = User.objects.get(username=username)
        
        other_calendar = Calendar.objects.create(title='Other Test Calendar', duration=30, creator=other_user)
        other_meeting = Meeting.objects.create(
            title='Other Test Meeting', receiver='other@example.com',
            status=False, start_time=datetime.now(), calendar=other_calendar
        )
        
        url = reverse('Calendar:meeting_edit', kwargs={'calendar_id': other_calendar.id, 'meeting_id': other_meeting.id})
        data = {
            'title': 'Updated Meeting',
            'receiver': 'update@example.com',
            'status': True,
            'start_time': datetime.now().isoformat()
        }
        response = self.client.put(url, data)
        print(response.data) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) ####

    def test_access_meeting_details_unauthenticated_user(self):
        self.client.logout()  # Make sure the client is not authenticated
        url = reverse('Calendar:meeting_details', kwargs={'calendar_id': self.calendar.id, 'meeting_id': self.meeting.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.other_user = User.objects.create_user(username='otheruser', password='testpassword')
        self.calendar = Calendar.objects.create(title='Test Calendar', duration=30, creator=self.user)
        self.meeting = Meeting.objects.create(
            title='Test Meeting', receiver='test@example.com',
            status=False, start_time=datetime.now(), calendar=self.calendar
        )
        self.client.force_authenticate(user=self.user)

    def test_create_meeting_with_invalid_data(self):
        url = reverse('Calendar:meeting_add', kwargs={'calendar_id': self.calendar.id})
        # Provide an invalid date format
        data = {
            'title': 'Invalid Data Meeting',
            'receiver': 'test@example.com',
            'status': False,
            'start_time': 'invalid-date-format'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('start_time', response.data)  # Check for validation error key

    def test_create_meeting_without_required_fields(self):
        url = reverse('Calendar:meeting_add', kwargs={'calendar_id': self.calendar.id})
        # Omit required fields
        data = {
            'title': '',  # Empty title
            'receiver': '',  # Empty receiver
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)  # Check for required field error key
        self.assertIn('receiver', response.data)

    def test_meeting_edit_permissions(self):
        self.client.force_authenticate(user=self.other_user)  # Authenticate as a different user
        url = reverse('Calendar:meeting_edit', kwargs={'calendar_id': self.calendar.id, 'meeting_id': self.meeting.id})
        data = {
            'title': 'Unauthorized Update Attempt',
            'receiver': 'test@example.com',
            'status': True,
            'start_time': datetime.now().isoformat()
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Check for permission denial

    def test_delete_meeting_with_wrong_user(self):
        self.client.force_authenticate(user=self.other_user)  # Authenticate as a different user
        url = reverse('Calendar:meeting_delete', kwargs={'calendar_id': self.calendar.id, 'meeting_id': self.meeting.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Check for permission denial
