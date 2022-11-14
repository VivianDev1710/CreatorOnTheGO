# from socket import fromshare
from django.forms import ModelForm
from django import forms
from .models import Video
import random

class UploadForm(ModelForm):
    # file=forms.FileField()
    # user=request.user
    user="N/A"
    caption=str(random.random()*200)
    video=forms.FileField()
    class Meta:
        model=Video
        fields=['video']

    

