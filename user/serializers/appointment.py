from datetime import timedelta, datetime

from rest_framework import serializers
from user.models import Appointment
from user.serializers.features import UserSerializer, AdvisorSerializer


class AppointmentSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    advisor = AdvisorSerializer(read_only=True)
    end_time = serializers.SerializerMethodField()
    class Meta:
        model = Appointment
        fields = [
            'id',
            'meet_url',
            'start_time',
            'end_time',
            'customer',
            'advisor',
        ]

    def get_end_time(self, obj):
        start_time = datetime.fromisoformat(obj.start_time.replace("Z", "+00:00"))
        end_time = start_time + timedelta(hours=1)
        return end_time.isoformat().replace("+00:00", "Z")
