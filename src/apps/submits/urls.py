from django.urls import path

from .views import (
    SubmissionDeleteView,
    SubmissionDetailView,
    SubmissionExportAllView,
    SubmissionExportView,
    SubmissionListView,
)

urlpatterns = [
    path("", SubmissionListView.as_view(), name="submits-list"),
    path("export/", SubmissionExportAllView.as_view(), name="submits-export-all"),
    path("<int:pk>/", SubmissionDetailView.as_view(), name="submits-detail"),
    path("<int:pk>/delete/", SubmissionDeleteView.as_view(), name="submits-delete"),
    path("<int:pk>/export/", SubmissionExportView.as_view(), name="submits-export"),
]
