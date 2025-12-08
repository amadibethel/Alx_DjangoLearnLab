# social_media_api/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Accounts app routes (register, login, profile)
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),

    # Posts & Comments API routes (required for task checks)
    path('posts/', include('posts.urls')),

    # DRF login/logout views (optional but recommended)
    path('api-auth/', include('rest_framework.urls')),
]

# Serve media files during development

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
