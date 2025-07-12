from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .tokens import MyAccessToken
from .models import *

class MyTokenObtainPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make username field accept email
        self.fields['username'].help_text = 'Username or Email'
    
    def validate(self, attrs):
        username_or_email = attrs.get('username')
        password = attrs.get('password')
        
        # Try to find user by email if it contains @
        if '@' in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
                # Replace username with actual username for authentication
                attrs['username'] = user.username
            except User.DoesNotExist:
                pass
        
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        access = MyAccessToken.for_user(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(access)
        data["user"] = UserSerializer(self.user).data

        return data
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser
        return token
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    

    class Meta:
        model = UserProfile
        fields = '__all__'

class EmotionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmotionRecord
        fields = "__all__"

class TodayStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TodayStory
        fields = "__all__"

class BlenderModelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlenderModels
        fields = "__all__"