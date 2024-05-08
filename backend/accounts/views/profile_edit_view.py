from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ProfileEditView(APIView):
    """
    API view for editing user profile information and password.
    Requires authentication for all methods.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieves the user's profile information.

        Returns:
            Response: User profile information including username, email, first name, and last name.
        """
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })

    def put(self, request):
        """
        Updates the user's profile information.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: Updated user profile information including username, email, first name, and last name.
        """
        user = request.user
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.email = request.data.get('email', user.email)
        user.save()
        return Response({
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })
    
    def patch(self, request):
        """
        Updates the user's password.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: Success message if the password is updated successfully, otherwise an error message.
        """
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if not old_password or not new_password:
            return Response({'error': 'Both old and new password are required'}, status=status.HTTP_400_BAD_REQUEST)
        if not check_password(old_password, user.password):
            return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)