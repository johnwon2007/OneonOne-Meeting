from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class ProfileDetailsView(APIView):
    """
    API view to retrieve profile details of an authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve profile details of the authenticated user.

        Returns:
            Response: JSON response containing the username, email, first name, and last name of the user.
        """
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })