from rest_framework import serializers
from coordinator.models import Scan

SCHEDULE_CHOICES = (
    ("Weekly", "Weekly"),
    ("Monthly", "Monthly"),
    ("Quarterly", "Quarterly"),
    ("Yearly", "Yearly"),
)


class ScanSerializer(serializers.ModelSerializer):
    schedule = serializers.ChoiceField(choices = SCHEDULE_CHOICES)
    class Meta:
        model = Scan
        fields = ['id', 'scanName', 'description', 'target', 'schedule', 'email']