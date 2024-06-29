from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile
from .models import ConvertedFile
from .serializers import ConvertedFileSerializer
import yt_dlp as youtube_dl
from PIL import Image
from io import BytesIO
import os
import requests

class ConvertYouTubeView(APIView):

    def get(self, request):
        # Recupera todos los archivos convertidos
        converted_files = ConvertedFile.objects.all()
        # Serializa los archivos
        serializer = ConvertedFileSerializer(converted_files, many=True)
        # Devuelve los datos serializados en la respuesta
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        video_url = request.data.get('url')
        if not video_url:
            return Response({'error': 'No URL provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Configura las rutas para archivos temporales
            temp_dir = 'C:\\temp' if os.name == 'nt' else '/tmp'
            audio_file_template = os.path.join(temp_dir, '%(id)s.%(ext)s')

            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '128',  # Calidad de audio mínima (en kbps)
                }],
                'outtmpl': audio_file_template,
                'noplaylist': True,
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=True)
                video_id = info_dict.get("id", None)
                audio_file_path = audio_file_template % {'id': video_id, 'ext': 'mp3'}

                # Extraer el título del video
                video_title = info_dict.get('title', None)

            # Verifica que el archivo de audio se haya creado
            if not os.path.exists(audio_file_path):
                return Response({'error': 'Audio file not found after conversion'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Descarga la imagen de portada
            thumbnail_url = info_dict.get('thumbnail', None)
            response = requests.get(thumbnail_url)
            img = Image.open(BytesIO(response.content))
            img_path = os.path.join(temp_dir, f'{video_id}.jpg')
            img.save(img_path, quality=50)  # Calidad mínima para la imagen (0-100)

            # Guarda los archivos en el modelo
            with open(audio_file_path, 'rb') as audio_file, open(img_path, 'rb') as cover_image:
                converted_file = ConvertedFile.objects.create(
                    video_url=video_url,
                    video_title=video_title,
                    audio_file=ContentFile(audio_file.read(), name=f'{video_id}.mp3'),
                    cover_image=ContentFile(cover_image.read(), name=f'{video_id}.jpg')
                )

            serializer = ConvertedFileSerializer(converted_file)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': f'Unable to process URL: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk=None):
            # Verifica que se haya proporcionado un id
            if not pk:
                return Response({'error': 'No ID provided'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Intenta recuperar el archivo convertido
                converted_file = ConvertedFile.objects.get(pk=pk)
                # Elimina los archivos asociados del sistema de archivos
                audio_file_path = converted_file.audio_file.path
                cover_image_path = converted_file.cover_image.path
                if os.path.exists(audio_file_path):
                    os.remove(audio_file_path)
                if os.path.exists(cover_image_path):
                    os.remove(cover_image_path)
                # Elimina el registro de la base de datos
                converted_file.delete()

                return Response({'message': 'File deleted successfully'}, status=status.HTTP_200_OK)
            except ConvertedFile.DoesNotExist:
                return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': f'Error deleting file: {str(e)}'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


