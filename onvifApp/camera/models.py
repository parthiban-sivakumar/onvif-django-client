from django.db import models
import json

# Create your models here.
class Camera(models.Model):

    ip = models.CharField(
    max_length=200, blank=False, null=False)
    port = models.CharField(max_length=200, blank=False)
    password = models.CharField(max_length=200, blank=False)
    username = models.CharField(max_length=200, blank=False)


    def __str__(self):
        return self.ip
      
    def __repr__(self):
        # Build a dict of values
        data = {
            "camera_ip": self.ip,
            "camera_port": self.port,
            "camera_username": self.username,
            "camera_password": self.password,
        }
        # Return JSON string
        return json.dumps(data)
      
    def save(self, *args, **kwargs):
      super(Camera, self).save(*args, **kwargs)