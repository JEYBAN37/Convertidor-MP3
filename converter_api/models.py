# models.py
from django.db import models

class ConvertedFile(models.Model):
    video_url = models.URLField()
    audio_file = models.FileField(upload_to='audios/')
    cover_image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    video_title = models.CharField(max_length=255)

    def __str__(self):
        return self.video_url
