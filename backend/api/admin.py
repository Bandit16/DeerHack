from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(EmotionRecord)
admin.site.register(TodayStory)
admin.site.register(Trauma)
admin.site.register(BlenderModels)