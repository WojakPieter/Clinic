from django.db import models

# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=255)

class User(models.Model):
    login = models.CharField(max_length=255)
    password = models.TextField()
    salt = models.TextField()
    role = models.ForeignKey(Role, on_delete=models.RESTRICT)

class Note(models.Model):
    patient = models.ForeignKey(User, related_name="note_patient", on_delete=models.CASCADE, blank=True, null=True)
    doctor = models.ForeignKey(User, related_name="note_doctor", on_delete=models.CASCADE, blank=True, null=True)
    creation_date = models.DateTimeField(blank=True, null=True)
    content = models.CharField(max_length=255)

class RefreshToken(models.Model):
    token = models.TextField()

class Visit(models.Model):
    patient = models.ForeignKey(User, related_name="visit_patient", on_delete=models.CASCADE, blank=True, null=True)
    doctor = models.ForeignKey(User, related_name="visit_doctor", on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    hour = models.IntegerField(blank=True, null=True)
