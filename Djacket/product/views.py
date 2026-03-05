from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Product, Job, Profile, Application
from .serializers import ProductSerializer, JobSerializer, ApplicationSerializer, ApplicationCreateSerializer

def index(request):
    return HttpResponse("Hello, Django.")

class LatestProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class JobList(APIView):
    def get(self, request, format=None):
        jobs = Job.objects.filter(is_open=True).order_by('-date_posted')
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        """Create a new job listing. Only company users can create jobs."""
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Get the user's profile
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            return Response(
                {"detail": "User profile not found."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user is a company
        if profile.user_type != 'company':
            return Response(
                {"detail": "Only company users can create jobs."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Create the job with the user's profile as company
        data = request.data.copy()
        serializer = JobSerializer(data=data)
        if serializer.is_valid():
            serializer.save(company=profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobDetail(APIView):
    def get_object(self, pk):
        try:
            return Job.objects.get(pk=pk, is_open=True)
        except Job.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        job = self.get_object(pk)
        serializer = JobSerializer(job)
        return Response(serializer.data)


class ApplicationList(APIView):
    """List all applications received by the logged-in company user."""
    def get(self, request, format=None):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            return Response({"detail": "User profile not found."}, status=status.HTTP_400_BAD_REQUEST)
        if profile.user_type != 'company':
            return Response({"detail": "Only company users can view applications."}, status=status.HTTP_403_FORBIDDEN)
        
        apps = Application.objects.filter(job__company=profile).order_by('-created_at')
        serializer = ApplicationSerializer(apps, many=True, context={'request': request})
        return Response(serializer.data)


class ApplicationDetail(APIView):
    """Retrieve (and optionally update) a single application for the company user."""
    def get_object(self, pk, profile):
        try:
            return Application.objects.get(pk=pk, job__company=profile)
        except Application.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            return Response({"detail": "User profile not found."}, status=status.HTTP_400_BAD_REQUEST)
        if profile.user_type != 'company':
            return Response({"detail": "Only company users can view applications."}, status=status.HTTP_403_FORBIDDEN)
        
        app = self.get_object(pk, profile)
        serializer = ApplicationSerializer(app, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        # allow company to update status
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            return Response({"detail": "User profile not found."}, status=status.HTTP_400_BAD_REQUEST)
        if profile.user_type != 'company':
            return Response({"detail": "Only company users can modify applications."}, status=status.HTTP_403_FORBIDDEN)
        
        app = self.get_object(pk, profile)
        # only status field can be updated
        status_value = request.data.get('status')
        if status_value not in dict(Application.STATUS_CHOICES):
            return Response({"status": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)
        app.status = status_value
        app.save()
        return Response(ApplicationSerializer(app).data)

class JobApply(APIView):
    def post(self, request, pk, format=None):
        """Submit a job application. Only individual users can apply."""
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Get the job
        try:
            job = Job.objects.get(pk=pk, is_open=True)
        except Job.DoesNotExist:
            raise Http404
        
        # Get the user's profile
        try:
            applicant = request.user.profile
        except Profile.DoesNotExist:
            return Response(
                {"detail": "User profile not found."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user is an individual
        if applicant.user_type != 'individual':
            return Response(
                {"detail": "Only individual users can apply for jobs."},
                status=status.HTTP_403_FORBIDDEN
            )

        data = request.data.copy()
        serializer = ApplicationCreateSerializer(data=data)
        if serializer.is_valid():
            application = serializer.save(job=job, applicant=applicant)
            return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
