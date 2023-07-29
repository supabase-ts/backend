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
            'account_no',
            'token',
        )

    def to_internal_value(self, data):
        # Map the incoming keys to the serializer field names
        data['password'] = data.pop('loginPassword', None)
        data['ktp_id'] = data.pop('ktpId', None)
        data['phone_number'] = data.pop('phoneNumber', None)
        data['birth_date'] = data.pop('birthDate', None)

        return super().to_internal_value(data)

    def validate(self, attrs):
        # Register
        url_register = "http://34.101.154.14:8175/hackathon/user/auth/create"
        url_login = "http://34.101.154.14:8175/hackathon/user/auth/token"
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
        response = requests.post(url_register, headers=headers, json=payload)

        print(response.json())

        if not response.json()['success']:
            raise serializers.ValidationError('Error in external registration')

        login_payload = {"username": attrs['username'], "loginPassword": attrs['password']}
        login_response = requests.post(url_login, headers=headers, json=login_payload)
        login_data = login_response.json()
        if login_response.status_code == 200 and login_data['success']:
            attrs['token'] = login_data['data']['accessToken']
        else:
            raise serializers.ValidationError('Error in getting token after registration')

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        # If the user is an advisor, create an Advisor instance
        if validated_data.get('is_advisor', False):
            Advisor.objects.create(user=user)

        # Create bank account for the user
        url = "http://34.101.154.14:8175/hackathon/bankAccount/create"
        payload = {"balance": 0}  # Initially set the balance to 0
        headers = {'Authorization': f'Bearer {user.token}', 'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            if data['success']:
                user.account_no = data['data']['accountNo']
                user.save()
            else:
                raise serializers.ValidationError('Error in external bank account creation')
        else:
            raise serializers.ValidationError('Error in external bank account creation')

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
