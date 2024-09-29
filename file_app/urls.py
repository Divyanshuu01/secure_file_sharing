from django.urls import path
from .views import SignupView, EmailVerifyView, UploadFileView, DownloadFileView, ListFilesView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('verify/<str:encrypted_url>/', EmailVerifyView.as_view(), name='email_verify'),
    path('upload/', UploadFileView.as_view(), name='upload_file'),
    path('download/<int:file_id>/', DownloadFileView.as_view(), name='download_file'),
    path('files/', ListFilesView.as_view(), name='list_files'),
]

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
