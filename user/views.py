from datetime import datetime

import requests
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def register(request):
    pass
    # # Extract data from the request
    # data = request.data
    #
    # # Make the request to the third-party API
    # url = 'http://34.101.154.14:8175/hackathon/user/auth/create'
    # response = requests.post(url, json=data)
    #
    # # If the request was successful
    # if response.status_code == 200:
    #     user, created = User.objects.get_or_create(
    #         username=data['username'],
    #         defaults={'email': data['email'], 'password': data['loginPassword']}
    #     )
    #
    #     profile, profile_created = Profile.objects.get_or_create(user=user)
    #
    #     profile.ktpId = data['ktpId']
    #     profile.phoneNumber = data['phoneNumber']
    #     profile.gender = data['gender']
    #     profile.save()
    #
    #     return Response({"status": "User created successfully"}, status=status.HTTP_201_CREATED)
    # else:
    #     return Response({"error": "Failed to create user"}, status=status.HTTP_400_BAD_REQUEST)

