from django.db import models


class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)


SCHEDULE_CHOICES = (
    ("Weekly", "Weekly"),
    ("Monthly", "Monthly"),
    ("Quarterly", "Quarterly"),
    ("Yearly", "Yearly"),
)


class Scan(models.Model):
    scanName = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    target = models.CharField(max_length=255, null=True)
    schedule = models.CharField(max_length=255, choices = SCHEDULE_CHOICES, default='Weekly')
    date = models.DateField(auto_now_add=True, null=True)
    email = models.EmailField(max_length=255, null=True)

    def __str__(self):
        return f"{self.scanName}"