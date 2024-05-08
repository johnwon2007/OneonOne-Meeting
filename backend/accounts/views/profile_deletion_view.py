from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class ProfileDeletionView(APIView):
    """
    API view for deleting a user profile.

    Only authenticated users can access this view.
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request):
        """
        Delete the user profile.

        Returns:
            Response: A response indicating the success or failure of the deletion.
        """
        user = request.user
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)