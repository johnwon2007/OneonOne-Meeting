from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from accounts.forms import RegisterForm
from django.db import IntegrityError
import traceback, json

class RegisterView(APIView):
    """
    API view for user registration.

    This view handles the registration of a new user by receiving a POST request
    with the following parameters:
    - username: The desired username for the new user.
    - password1: The password for the new user.
    - password2: The confirmation password for the new user.
    - email: The email address for the new user.
    - first_name: The first name of the new user.
    - last_name: The last name of the new user.

    If any of the required fields are missing or the passwords do not match,
    an error response is returned. Otherwise, a new user is created and a success
    response is returned.

    HTTP Methods:
    - POST: Create a new user.

    Returns:
    - 201 Created: If the user is created successfully.
    - 400 Bad Request: If any of the required fields are missing or the passwords do not match.
    """

    

    def post(self, request):
        try:
            form = RegisterForm(json.loads(request.body))
            if form.is_valid():
                User.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data.get('email'),
                    first_name=form.cleaned_data.get('phone'),  # doesn't matter
                    password=form.cleaned_data['password1'],
                )
                return JsonResponse({'message' : "User added."})
        except IntegrityError:
            return JsonResponse({'message' : "Username already exists."}, status=409)
        except:
            traceback.print_exc()
        # handles any error or invalid form
        return JsonResponse({'message' : "Unknown error."}, status=400)
        