from rest_framework import serializers
from coordinator.models import Scan

# schedule choices creates a dropdown menu of schedule options
SCHEDULE_CHOICES = (
    ("Weekly", "Weekly"),
    ("Monthly", "Monthly"),
    ("Quarterly", "Quarterly"),
    ("Yearly", "Yearly"),
)

# serializer class takes in Scan as the model in the meta class so that it can serialize the Scan model
# schedule is declared as a property here so that we can have a dropdown menu
class ScanSerializer(serializers.ModelSerializer):
    schedule = serializers.ChoiceField(choices = SCHEDULE_CHOICES)
    class Meta:
        model = Scan
        fields = ['id', 'scanName', 'description', 'target', 'schedule', 'userEmail']