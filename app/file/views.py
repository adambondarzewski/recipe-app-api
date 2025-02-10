from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from file.models import File
from django.http import FileResponse
import os


class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        if not file:
            return Response(
                {"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        uploaded_file = File.objects.create(file=file)  # Saves file using FileField

        return Response(
            {
                "message": "File uploaded successfully",
                "file_id": uploaded_file.id,
                "file_url": uploaded_file.file.url,  # Returns file URL
            },
            status=status.HTTP_201_CREATED,
        )


class FileDownloadView(APIView):
    def get(self, request, file_id, *args, **kwargs):
        if not file_id:
            return Response(
                {"error": "No file ID provided"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            uploaded_file = File.objects.get(id=file_id)
        except File.DoesNotExist:
            return Response(
                {"error": "File not found"}, status=status.HTTP_404_NOT_FOUND
            )

        file_path = uploaded_file.file.path

        return FileResponse(
            open(file_path, "rb"),
            as_attachment=True,
            filename=os.path.basename(file_path),
        )
