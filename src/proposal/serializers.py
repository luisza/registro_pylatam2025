from rest_framework import serializers

from proposal.models import SpeechSchedule


class SpeechScheduleSerializer(serializers.ModelSerializer):
    html_id = serializers.CharField(validators=[])

    class Meta:
        model = SpeechSchedule
        fields = '__all__'
