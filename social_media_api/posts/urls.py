# posts/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),   # your accounts
    path('api/', include('posts.urls')),
    path('feed/', FeedView.as_view(), name='feed'),
    path('posts/', include('posts.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# social_media_api/urls.py (add)
path('api/', include('posts.urls')),
