# posts/views.py
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .serializers import PostListSerializer, PostDetailSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from .pagination import StandardResultsSetPagination

class PostViewSet(viewsets.ModelViewSet):
    """
    list: GET /api/posts/
    retrieve: GET /api/posts/{pk}/
    create: POST /api/posts/
    update/partial_update: PUT/PATCH /api/posts/{pk}/
    destroy: DELETE /api/posts/{pk}/
    """
    queryset = Post.objects.select_related('author').prefetch_related('comments').all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']  # basic DRF search
    ordering_fields = ['created_at', 'updated_at']

    def get_serializer_class(self):
        if self.action in ['list']:
            return PostListSerializer
        return PostDetailSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        """
        Custom search endpoint: /api/posts/search/?q=keyword
        (Also available via DRF SearchFilter on list.)
        """
        q = request.GET.get('q', '')
        if not q:
            return Response({'detail': 'Provide a "q" query parameter.'}, status=status.HTTP_400_BAD_REQUEST)
        qs = Post.objects.filter(Q(title__icontains=q) | Q(content__icontains=q)).distinct()
        page = self.paginate_queryset(qs)
        serializer = PostListSerializer(page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    """
    list: GET /api/comments/             (global list, paginated)
    retrieve: GET /api/comments/{pk}/
    create: POST /api/comments/         (post must be passed in body)
    update/partial_update: PUT/PATCH /api/comments/{pk}/
    destroy: DELETE /api/comments/{pk}/
    """
    queryset = Comment.objects.select_related('author', 'post').all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content']
    ordering_fields = ['created_at', 'updated_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
