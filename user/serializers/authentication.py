import requests
from django.contrib.auth import authenticate
from rest_framework import serializers

from user.models import User, Advisor


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'email',
            'is_advisor',
            'ktp_id',
            'phone_number',
            'birth_date',
            'gender',
        )

    def to_internal_value(self, data):
        # Map the incoming keys to the serializer field names
        data['password'] = data.pop('loginPassword', None)
        data['ktp_id'] = data.pop('ktpId', None)
        data['phone_number'] = data.pop('phoneNumber', None)
        data['birth_date'] = data.pop('birthDate', None)

        return super().to_internal_value(data)

    def validate(self, attrs):
        url = "http://34.101.154.14:8175/hackathon/user/auth/create"
        payload = {
            "ktpId": attrs['ktp_id'],
            "username": attrs['username'],
            "phoneNumber": attrs['phone_number'],
            "loginPassword": attrs['password'],
            "birthDate": attrs.get('birth_date', ''),  # If 'birth_date' is not provided, it will use empty string
            "gender": attrs.get('gender', 1),  # If 'gender' is not provided, it will use 1
            "email": attrs['email'],
            "is_advisor": attrs['is_advisor'],
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=payload)

        if not response.json()['success']:
            raise serializers.ValidationError('Error in external registration')

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        # If the user is an advisor, create an Advisor instance
        if validated_data.get('is_advisor', False):
            Advisor.objects.create(user=user)

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def to_internal_value(self, data):
        data['password'] = data.pop('loginPassword', None)

        return super().to_internal_value(data)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        # Authenticate user with the external API
        url = "http://34.101.154.14:8175/hackathon/user/auth/token"
        payload = {"username": username, "loginPassword": password}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=payload)

        # If the external API returns success, authenticate the user with Django
        if response.json().get('success'):
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                # Return both the authenticated user and the access token from the external API
                return {'user': user, 'access_token': response.json()['data']['accessToken']}
            else:
                raise serializers.ValidationError("Invalid username/password.")
        else:
            raise serializers.ValidationError("Error in external authentication")

    def create(self, validated_data):
        return validated_data
