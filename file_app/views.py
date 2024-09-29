from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.core.mail import send_mail
from .models import User, File
from .serializers import UserSerializer, FileSerializer
from django.conf import settings
from django.utils.crypto import get_random_string

# Sign Up View
class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()
            encrypted_url = get_random_string(length=32)  # Generate encrypted link
            send_mail(
                'Verification Email',
                f'Please verify your email by clicking this link: {settings.BASE_URL}/verify/{encrypted_url}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return Response({"encrypted_url": encrypted_url, "message": "success"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Email Verification View
class EmailVerifyView(APIView):
    def get(self, request, encrypted_url):
        # Here you would verify the email address using the encrypted_url
        return Response({"message": "Email Verified Successfully"})

# Upload File (Ops User only)
class UploadFileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.user_type != 'operation':
            return Response({"message": "You do not have permission to upload files."}, status=status.HTTP_403_FORBIDDEN)

        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            file_obj = request.FILES['file']
            if file_obj.content_type not in File.allowed_types:
                return Response({"message": "Invalid file type."}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save(uploaded_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Download File (Client User only)
class DownloadFileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, file_id):
        try:
            file = File.objects.get(id=file_id)
            if request.user.user_type != 'client':
                return Response({"message": "Only clients are allowed to download files."}, status=status.HTTP_403_FORBIDDEN)

            download_link = f"{settings.BASE_URL}/media/{file.file.name}"
            return Response({"download-link": download_link, "message": "success"}, status=status.HTTP_200_OK)
        except File.DoesNotExist:
            return Response({"message": "File not found."}, status=status.HTTP_404_NOT_FOUND)

# List all uploaded files (Client User only)
class ListFilesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.user_type != 'client':
            return Response({"message": "Only clients are allowed to view files."}, status=status.HTTP_403_FORBIDDEN)

        files = File.objects.filter(uploaded_by__user_type='operation')
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)
