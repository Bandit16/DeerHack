from rest_framework_simplejwt.tokens import AccessToken

class MyAccessToken(AccessToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        # 🔧 Add custom claims here

        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser
        return token
