from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from plagiarism import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
