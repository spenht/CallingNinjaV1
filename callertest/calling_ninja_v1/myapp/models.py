from django.db import models

class Call(models.Model):
    phone_number = models.CharField(max_length=15)
    call_date = models.DateTimeField(auto_now_add=True)
    audio_file = models.FileField(upload_to='audio/')
    status = models.CharField(max_length=30)
