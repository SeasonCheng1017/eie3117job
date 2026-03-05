from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Profile, Job, Application


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "user_type",
            "nickname",
            "profile_image",
            "company_name",
            "website",
        )


class CustomUserCreateSerializer(serializers.ModelSerializer):
    """Custom serializer for user registration that handles profile fields."""
    user_type = serializers.CharField(write_only=True, required=True)
    nickname = serializers.CharField(write_only=True, required=True)
    profile_image = serializers.ImageField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'user_type', 'nickname', 'profile_image')
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        # debug logging
        print('CustomUserCreateSerializer.create called with', validated_data)
        user_type = validated_data.pop('user_type', None)
        nickname = validated_data.pop('nickname', None)
        profile_image = validated_data.pop('profile_image', None)
        
        user = User.objects.create_user(**validated_data)
        
        # Update or create profile
        profile, created = Profile.objects.get_or_create(user=user)
        if user_type:
            profile.user_type = user_type
        if nickname:
            profile.nickname = nickname
        if profile_image:
            profile.profile_image = profile_image
        profile.save()
        
        return user


class CustomUserSerializer(serializers.ModelSerializer):
    """Custom serializer for user profile that includes the profile data."""
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'profile')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "description",
            "price",
            "get_image",
            "get_thumbnail",
        )


class JobSerializer(serializers.ModelSerializer):
    company = ProfileSerializer(read_only=True)

    class Meta:
        model = Job
        fields = (
            "id",
            "title",
            "requirement",
            "duty",
            "salary",
            "location",
            "date_posted",
            "is_open",
            "company",
        )


class ApplicationSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    applicant = ProfileSerializer(read_only=True)

    class Meta:
        model = Application
        fields = (
            "id",
            "job",
            "applicant",
            "message",
            "cv",
            "created_at",
            "status",
        )
        
class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ("id", "job", "message", "cv")
        extra_kwargs = {
            "job": {"read_only": True},
        }

