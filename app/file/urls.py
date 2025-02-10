"""URL mappings for the File app."""

from django.urls import path

from .views import FileUploadView
from .views import FileDownloadView

app_name = "file"

urlpatterns = urlpatterns = [
    path("upload", FileUploadView.as_view(), name="upload"),
    path("download/<int:file_id>/", FileDownloadView.as_view(), name="download"),
]
