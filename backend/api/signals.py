from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print(f"Created UserProfile for user: {instance.username}")
    else:
        # Only save if the profile exists to avoid errors
        try:
            instance.profile.save()
            print(f"Updated UserProfile for user: {instance.username}")
        except UserProfile.DoesNotExist:
            # Create profile if it doesn't exist
            UserProfile.objects.create(user=instance)
            print(f"Created missing UserProfile for user: {instance.username}")
# This signal ensures that a UserProfile is created or updated whenever a User is created or updated.