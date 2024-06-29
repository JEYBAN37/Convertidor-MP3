from django.urls import path
from .views import ConvertYouTubeView

urlpatterns = [
    path('convert/', ConvertYouTubeView.as_view(), name='convert'),
    path('convert/<int:pk>/', ConvertYouTubeView.as_view(), name='convert_youtube_delete'),

]
