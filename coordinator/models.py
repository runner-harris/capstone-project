from django.db import models

class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)

class Scan(models.Model):
    scanName = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    target = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.scanName}"