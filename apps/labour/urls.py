from django.urls import path
from apps.labour import views

app_name = "labour"

urlpatterns = [
    # Labour profile
    path("profile/", views.LabourProfileView.as_view(), name="profile"),

    # Job management
    path("jobs/", views.JobListView.as_view(), name="job-list"),
    path("jobs/create/", views.JobCreateView.as_view(), name="job-create"),
    path("jobs/history/", views.JobHistoryView.as_view(), name="job-history"),
    path("jobs/<str:job_id>/", views.JobDetailView.as_view(), name="job-detail"),
    path("jobs/<str:job_id>/accept/", views.JobAcceptView.as_view(), name="job-accept"),
    path("jobs/<str:job_id>/complete/", views.JobCompleteView.as_view(), name="job-complete"),
    path("jobs/<str:job_id>/reject/", views.JobRejectView.as_view(), name="job-reject"),

    # Nearby & search
    path("nearby/", views.NearbyLabourView.as_view(), name="nearby"),
    path("hire/", views.DirectHireView.as_view(), name="hire"),
]
