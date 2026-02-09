from rest_framework import serializers
from .models import Product, Profile, Job, Application


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

