from django.db import models


class File(models.Model):
    """File object"""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="uploads/")

    def __str__(self):
        return self.name
