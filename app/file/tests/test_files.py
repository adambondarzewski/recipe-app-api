import os
import tempfile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from file.models import UploadedFile


class FileUploadDownloadTests(APITestCase):
    def setUp(self):
        # Set up any necessary data for tests
        self.upload_url = reverse("file-upload")
        self.download_url = reverse("file-download", args=[1])

    def test_file_upload(self):
        """Test uploading a file through the API."""
        file_content = b"Test file content."
        uploaded_file = SimpleUploadedFile(
            "testfile.txt", file_content, content_type="text/plain"
        )

        response = self.client.post(
            self.upload_url, {"file": uploaded_file}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("file", response.data)  # Ensure response includes file metadata
        self.assertTrue(UploadedFile.objects.filter(id=response.data["id"]).exists())

    def test_file_download(self):
        """Test downloading a file through the API."""
        # First, create a file entry in the database
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(b"Temporary file content.")
        temp_file.close()

        uploaded_file = UploadedFile.objects.create(
            file=temp_file.name, filename="tempfile.txt"
        )

        response = self.client.get(reverse("file-download", args=[uploaded_file.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b"Temporary file content.")

        # Cleanup the temporary file
        os.remove(temp_file.name)

    def test_file_upload_invalid(self):
        """Test uploading an invalid file."""
        response = self.client.post(self.upload_url, {}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "file", response.data
        )  # Ensure error message refers to missing file

    def test_file_not_found(self):
        """Test downloading a non-existent file."""
        response = self.client.get(
            reverse("file-download", args=[9999])
        )  # Non-existent file ID

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_file_upload_large_file(self):
        """Test uploading a large file."""
        large_file_content = b"A" * (10 * 1024 * 1024)  # 10 MB file
        uploaded_file = SimpleUploadedFile(
            "largefile.txt", large_file_content, content_type="text/plain"
        )

        response = self.client.post(
            self.upload_url, {"file": uploaded_file}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("file", response.data)
