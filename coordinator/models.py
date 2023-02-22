from django.db import models

# User was just a test function
class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)

# Scan is a function that creates a scan object
class Scan(models.Model):
    scanName = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    target = models.CharField(max_length=255, null=True)
    # the below function makes the scan object in the admin page more user friendly
    def __str__(self):
        return f"{self.scanName}"