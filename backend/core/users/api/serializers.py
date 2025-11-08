from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        token['full_name'] = user.full_name
        token['avatar'] = user.avatar or ''
        token['oauth_provider'] = user.oauth_provider or ''
        token['verified_author'] = user.verified_author
        token['theme_preference'] = user.theme_preference
        token['writing_style'] = user.writing_style
        token['preferred_language'] = user.preferred_language
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser
        return token
    

class SocialAuthSerializer(serializers.Serializer):
    provider = serializers.ChoiceField(choices=['google', 'github'])
    access_token = serializers.CharField()

