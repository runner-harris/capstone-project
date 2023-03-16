from django.db import models

# User to be worked with later
class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)


SCHEDULE_CHOICES = (
    ("Weekly", "Weekly"),
    ("Monthly", "Monthly"),
    ("Quarterly", "Quarterly"),
    ("Yearly", "Yearly"),
)
# Scan is a function that creates a scan object
class Scan(models.Model):
    scanName = models.CharField(max_length=255, null=True)
    description = models.TextField()
    target = models.CharField(max_length=255, null=True)
    schedule = models.CharField(max_length=255, choices = SCHEDULE_CHOICES, default='Weekly')
    date = models.DateField(auto_now_add=True, null=True)
    # the below function makes the scan object in the admin page more user friendly
    def __str__(self):
        return f"{self.scanName}"