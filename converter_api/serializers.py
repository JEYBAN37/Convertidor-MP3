from rest_framework import serializers
from .models import ConvertedFile

class ConvertedFileSerializer(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField()
    audio_file = serializers.SerializerMethodField()

    def get_cover_image(self, obj):
        return obj.cover_image.url if obj.cover_image else None

    def get_audio_file(self, obj):
        return obj.audio_file.url if obj.audio_file else None

    class Meta:
        model = ConvertedFile
        fields = ['id', 'video_url', 'audio_file', 'cover_image','video_title']
