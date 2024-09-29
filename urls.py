from django.urls import path, include

urlpatterns = [
    path('api/', include('file_app.urls')),
]
