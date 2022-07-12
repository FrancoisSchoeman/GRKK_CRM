from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('mailer/', include('mailer.urls')),
    path('tinymce/', include('tinymce.urls')),
]
