from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('latest-products/', views.LatestProductsList.as_view()),
    path('jobs/', views.JobList.as_view(), name="job-list"),
    path('jobs/<int:pk>/', views.JobDetail.as_view(), name="job-detail"),
    path("jobs/<int:pk>/apply/", views.JobApply.as_view(), name="job-apply"),
]