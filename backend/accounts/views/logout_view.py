from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView, status
from rest_framework.response import Response

class LogoutView(APIView):
    def post(self, request):
        """
        Handle the logout functionality by invalidating the provided refresh token.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object with a success message if logout is successful,
                      or an error message if an exception occurs.
        """
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)