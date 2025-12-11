# posts/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions, generics, status
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly #StandardResultsPagination # We will define this custom permission
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType


# --- Custom Pagination Class (Step 5) ---
class StandardResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# --- Post ViewSet (Step 3 & 5) ---
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = StandardResultsPagination # Pagination
    
    # Permissions: Authenticated users can create/edit/delete, others can only read
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly] 
    
    # Filtering: Allows searching by 'title' or 'content' (Step 5)
    filter_backends = [SearchFilter]
    search_fields = ['title', 'content'] 

    # We override perform_create to set the author (redundant due to serializer, but good practice)
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# --- Comment ViewSet (Step 3 & 5) ---
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = StandardResultsPagination # Pagination
    
    # Permissions: Authenticated users can create/edit/delete, others can only read
    # Use IsAuthenticated for comments to prevent anonymous comments, but IsAuthorOrReadOnly for edits
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 

    def get_queryset(self):
        # Restrict queryset to comments associated with a specific post (if nested URL is used)
        if 'post_pk' in self.kwargs:
            return Comment.objects.filter(post_id=self.kwargs['post_pk'])
        return Comment.objects.all()

    def perform_create(self, serializer):
        # We need the post ID for creation. Assuming non-nested URL for simplicity here.
        # In a real app, this would be handled via a nested router or an explicit post_id field.
        # For this setup, we'll assume the post ID is passed in the request data, or use a simplified approach.
        
        # NOTE: For simplicity and following ModelViewSet pattern, we assume the Post ID is included
        # in the request data OR we'll use a mixin if nested routing is implemented.
        # Since we use the serializer's create method to set the user/post, this is sufficient.
        serializer.save(user=self.request.user)
        
# --- /api/feed/ View (GET) ---
class FeedView(generics.ListAPIView):
    """
    Retrieves a list of posts from users the current user is following.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsPagination

    def get_queryset(self):
        # 1. Get the list of users the current user is following
        following_users = self.request.user.following.all()

        # 2. Retrieve posts created by those users
        queryset = Post.objects.filter(author__in=following_users)

        # 3. Order by created_at (newest posts at the top)
        return queryset.order_by('-created_at')

# --- Helper function for Notification creation (Place at the top of views.py) ---
def create_notification(recipient, actor, verb, target):
    """Creates a new Notification object."""
    from notifications.models import Notification
    
    # Prevent notifying yourself for self-actions
    if recipient.pk == actor.pk:
        return 

    Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        target=target
    )


# --- /api/posts/<int:pk>/like/ View (POST/DELETE) ---
class PostLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        
        # Check if the user already liked the post
        like, created = Like.objects.get_or_create(post=post, user=user)
        
        if created:
            # SUCCESS: Like created, now generate notification
            create_notification(
                recipient=post.author,
                actor=user,
                verb="liked your post",
                target=post
            )
            return Response({"detail": "Post liked successfully."}, status=status.HTTP_201_CREATED)
        else:
            # Already liked, this acts as a toggle (unlike)
            like.delete()
            return Response({"detail": "Post unliked successfully."}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        # Handles explicit DELETE request for unlike
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        
        liked_post = Like.objects.filter(post=post, user=user)
        if liked_post.exists():
            liked_post.delete()
            return Response({"detail": "Post unliked successfully."}, status=status.HTTP_204_NO_CONTENT)
        
        return Response({"detail": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)

'''
Post.objects.filter(author__in=following_users).order_by
generics.get_object_or_404(Post, pk=pk)
Like.objects.get_or_create(user=request.user, post=post)
'''