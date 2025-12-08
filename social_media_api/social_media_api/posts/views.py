# posts/views.py
from django.db.models import Q
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from .models import Post, Comment
from .serializers import PostListSerializer, PostDetailSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from .pagination import StandardResultsSetPagination

# IMPORTANT: explicit QuerySets to satisfy checks
POST_QS = Post.objects.all()
COMMENT_QS = Comment.objects.all()


class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD for Posts. Includes a feed action that returns posts from users
    the requesting user follows (ordered by created_at desc).
    """
    queryset = POST_QS.order_by('-created_at')
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return PostDetailSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        q = request.GET.get('q', '')
        if not q:
            return Response({'detail': 'Provide a "q" query parameter.'}, status=status.HTTP_400_BAD_REQUEST)
        qs = POST_QS.filter(Q(title__icontains=q) | Q(content__icontains=q)).distinct().order_by('-created_at')
        page = self.paginate_queryset(qs)
        serializer = PostListSerializer(page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=['get'], url_path='feed', permission_classes=[permissions.IsAuthenticated])
    def feed(self, request):
        """
        /api/posts/feed/ -> posts authored by users the current user follows.
        Requires authentication.
        """
        user = request.user
        # Expect user.following to be the users this user follows (depends on your User model)
        following_qs = user.following.all()  # assumes User.following ManyToMany exists
        if not following_qs.exists():
            return self.get_paginated_response([])

        qs = POST_QS.filter(author__in=following_qs).order_by('-created_at')
        page = self.paginate_queryset(qs)
        serializer = PostListSerializer(page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD for Comments.
    """
    queryset = COMMENT_QS.order_by('created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content']
    ordering_fields = ['created_at', 'updated_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
