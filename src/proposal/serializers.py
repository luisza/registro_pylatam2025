from rest_framework import serializers

from proposal.models import SpeechSchedule


class SpeechScheduleSerializer(serializers.Serializer):
    class Meta:
        model = SpeechSchedule
        fields = '__all__'
