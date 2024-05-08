from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.views import APIView


class LoginView(APIView):
    def post(self, request):
        """
        Handle the POST request for user login.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - If the user is authenticated, returns a response containing the refresh and access tokens.
        - If the user is not authenticated, returns a response with an error message and status code 400.
        """
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid Credentials'}, status=400)
        
