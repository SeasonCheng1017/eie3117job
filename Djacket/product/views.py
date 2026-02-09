from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Product, Job
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

class JobApply(APIView):
    def post(self, request, pk, format=None):
        try:
            job = Job.objects.get(pk=pk, is_open=True)
        except Job.DoesNotExist:
            raise Http404

        # In a real app, use the logged-in user's Profile as applicant.
        # For now, expect applicant_profile_id from the request.
        applicant_profile_id = request.data.get("applicant_profile_id")
        if not applicant_profile_id:
            return Response(
                {"detail": "applicant_profile_id is required"},
                status=400,
            )

        try:
            applicant = Profile.objects.get(pk=applicant_profile_id, user_type="individual")
        except Profile.DoesNotExist:
            return Response(
                {"detail": "Invalid applicant_profile_id"},
                status=400,
            )

        data = request.data.copy()
        serializer = ApplicationCreateSerializer(data=data)
        if serializer.is_valid():
            application = serializer.save(job=job, applicant=applicant)
            return Response(ApplicationSerializer(application).data, status=201)
        return Response(serializer.errors, status=400)
