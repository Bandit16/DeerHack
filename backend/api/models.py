from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification

# Load once
processor = AutoImageProcessor.from_pretrained("dima806/facial_emotions_image_detection")
model = AutoModelForImageClassification.from_pretrained("dima806/facial_emotions_image_detection")
model.eval()

class Trauma(models.Model):
    title= models.CharField(max_length=100)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE , related_name='profile')

    profile_pic = ResizedImageField(size=[1080, 1080], quality=90,
                                    upload_to="customer_images/", default='default.webp')
    trauma = models.ForeignKey(Trauma, on_delete=models.CASCADE, related_name='profiles',default=1, null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    

    def __str__(self):
        return self.user.username
    
class EmotionRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emotion_records')
    timestamp = models.DateTimeField(auto_now_add=True)
    dominant_emotion = models.CharField(max_length=30)
    emotion_scores = models.JSONField()  # Stores all scores: {happy: 0.8, sad: 0.1, ...}
    session_id = models.CharField(max_length=100, null=True, blank=True)  # Optional: for grouping

    def __str__(self):
        return f"{self.user.username} - {self.dominant_emotion} @ {self.timestamp}"

class TodayStory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='today_stories')
    story_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Story for {self.user.username} on {self.created_at.strftime('%Y-%m-%d')}"

class BlenderModels(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='blender_models/')

    def __str__(self):
        return self.name