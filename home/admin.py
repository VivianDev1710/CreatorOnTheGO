from django.contrib import admin

# Register your models here.
from .models import Video
from .models import Text
admin.site.register(Video)
admin.site.register(Text)