from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=500)
    image = models.URLField(max_length=500)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(primary_key=True, editable=False)