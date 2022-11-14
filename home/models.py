import datetime
from django.db import models
from django.utils.timezone import now
from colorfield.fields import ColorField

# Create your models here.
class Video(models.Model):
    caption=models.CharField(max_length=100)
    video=models.FileField(upload_to="video/%y")
    user=models.TextField(max_length=150)
    x_crop=models.IntegerField(default=0)
    from_time=models.IntegerField(default=-1)
    to_time=models.IntegerField(default=-1)
    face=models.BooleanField(default=True)
    audio=models.BooleanField(default=True)
    filter=models.IntegerField(default=0)
    edited=models.BooleanField(default=False)
    def __str__(self):
        return self.caption+" by "+self.user

class Text(models.Model):
    textid=models.IntegerField(default=1)
    text=models.CharField(max_length=25)
    videoid=models.IntegerField()
    from_time=models.IntegerField(default=-1)
    to_time=models.IntegerField(default=-1)
    bgColor=ColorField(default='#FFFFFF')
    textColor=ColorField(default='#000000')
    def __str__(self):
        return self.text+" video:"+ str(self.videoid)
