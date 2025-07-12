
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from rest_framework.response import Response
from rest_framework import status , permissions, viewsets
from rest_framework.generics import ListAPIView

from rest_framework_simplejwt.views import TokenViewBase
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from .utils import *
from PIL import Image
from django.utils import timezone
from datetime import timedelta

@api_view(['GET', 'PUT', 'DELETE'])
def user_profile_view(request):
    

    if request.method == 'GET':
        profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(profiles , many=True)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        try:
            profile = request.user.profile  # via related_name='profile'
        except UserProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=404)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        profile.delete()
        return Response({'message': 'Profile deleted'}, status=204)

class EmotionDetectionView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]  # Allow any user to access this endpoint

    def post(self, request, format=None):
        print("Request FILES:", request.FILES)
        print("Request POST:", request.POST)
        print("Request data:", request.data)
        
        # Check for different possible field names
        image_file = None
        for field_name in ['frame', 'image', 'file']:
            if field_name in request.FILES:
                image_file = request.FILES[field_name]
                print(f"Found image in field: {field_name}")
                break
        
        if not image_file:
            return Response({
                "error": "No image uploaded.", 
                "available_fields": list(request.FILES.keys())
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            image = Image.open(image_file).convert("RGB")
            result = detect_emotion_from_image(image)
            EmotionRecord.objects.create(
            user=request.user,
            dominant_emotion=result["dominant_emotion"],
            emotion_scores=result["scores"],
            session_id=request.data.get("session_id")  # optional
        )

            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": "Error processing image", 
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmotionHistoryView(ListAPIView):
    serializer_class = EmotionRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = EmotionRecord.objects.filter(user=self.request.user).order_by('-timestamp')
        
        period = self.request.query_params.get('period', None)
        if period:
            now = timezone.now()
            if period == 'today':
                queryset = queryset.filter(timestamp__date=now.date())
            elif period == 'week':
                start_date = now.date() - timedelta(days=now.weekday())
                queryset = queryset.filter(timestamp__date__gte=start_date)
            elif period == 'month':
                queryset = queryset.filter(
                    timestamp__year=now.year,
                    timestamp__month=now.month
                )
                
        return queryset

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_daily_story(request):
    try:
        bio = request.user.profile.bio if hasattr(request.user, 'profile') else None
        if not bio:
            return Response({'error': 'bio is empty'}, status=status.HTTP_404_NOT_FOUND)
        
        trauma = request.user.profile.trauma if hasattr(request.user, 'profile') else None
        if not trauma:
            return Response({'error': 'trauma is empty'}, status=status.HTTP_404_NOT_FOUND)
        
        story_text = ask_gpt(
        user_message=(
            f"Write a short, uplifting story (under 250 words) inspired by this user's bio. "
            f"The user is dealing with severe PTSD related to: {trauma}. "
            f"Gently reflect aspects of their bio in the story, focusing on resilience, hope, and small personal victories. "
            f"The story should be emotionally supportive and help the user feel seen, safe, and motivated to move forward."
            f"\n\nUser Bio:\n{bio}"
        ),
        system_message=(
            "You are a compassionate storyteller who writes simple, heartwarming stories designed to gently encourage people dealing with trauma. "
            "Avoid triggering content. Focus on themes of strength, healing, and inner courage."
        )
    )

        
        # Fix: Use get_or_create properly
        today_story, created = TodayStory.objects.get_or_create(
            user=request.user, 
            defaults={'story_text': story_text}
        )
        
        # Fix: If not created (already exists), update with new story
        if not created:
            today_story.story_text = story_text
            today_story.save()

        # Fix: Use serializer properly - no need to pass data for reading
        serializer = TodayStorySerializer(today_story)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Error in get_daily_story: {str(e)}")
        return Response({'error': 'Failed to generate story', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_blender_models(request):
    try:
        models = BlenderModels.objects.all()
        serializer = BlenderModelsSerializer(models, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Error in get_blender_models: {str(e)}")
        return Response({'error': 'Failed to retrieve models', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)











class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://127.0.0.1:8000/accounts/google/login/callback/'
    client_class = OAuth2Client
    def post(self, request, *args, **kwargs):
        # Validate and complete social login
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)
        self.login()
        user = self.user

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access = MyTokenObtainPairSerializer.get_token(user)

        # Try to get profile pic from Google account if available
        profile_pic_url = None
        extra_data = getattr(user, 'socialaccount_set', None)
        if extra_data and extra_data.exists():
            google_account = extra_data.filter(provider='google').first()
            if google_account and 'picture' in google_account.extra_data:
                profile_pic_url = google_account.extra_data['picture']
            elif user.profile.profile_pic:
                profile_pic_url = user.profile.profile_pic.url
        else:
            profile_pic_url = user.profile.profile_pic.url if user.profile.profile_pic else None

        return Response({
            'access': str(access),
            'refresh': str(refresh),
            'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'profile_pic': profile_pic_url,
            }
        }, status=status.HTTP_200_OK)

class MyTokenObtainPairView(TokenViewBase):
    serializer_class = MyTokenObtainPairSerializer