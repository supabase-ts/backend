from rest_framework import serializers
from user.models import Advisor, Expertise, Availability, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'ktp_id',
            'phone_number',
            'account_no',
            'birth_date',
            'gender',
            'account_no',
        )


class ExpertiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expertise
        fields = ('name',)


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ('time',)


class AdvisorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    expertise = ExpertiseSerializer(many=True, read_only=True)
    availability = AvailabilitySerializer(many=True, read_only=True)

    class Meta:
        model = Advisor
        fields = (
            'user',
            'full_name',
            'profile_picture',
            'years_of_experience',
            'current_role',
            'current_employer',
            'rate_per_hour',
            'expertise',
            'availability'
        )
