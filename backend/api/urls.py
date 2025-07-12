from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', views.user_profile_view, name='user-profile'),
    path("detect/", EmotionDetectionView.as_view(), name="detect-emotion"),
    path("history/", EmotionHistoryView.as_view()),
    path("today-story/", get_daily_story, name="today-story"),
    path("blender-models/", get_blender_models, name="get-blender-models"),

]