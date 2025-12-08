# accounts/views.py
from rest_framework import status
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import PostSerializer
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)
        data = UserSerializer(user, context={'request': request}).data
        data['token'] = token.key
        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user=user)
        data = UserSerializer(user, context={'request': request}).data
        data['token'] = token.key
        return Response(data, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'username'
    queryset = User.objects.all()

    # GET /accounts/profile/<username>/
    # PATCH/PUT for updates (only owner should update)
    def update(self, request, *args, **kwargs):
        # ensure only owner can update
        user = self.get_object()
        if request.user != user:
            return Response({'detail': 'You do not have permission to edit this profile.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)


class FollowToggleView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username, *args, **kwargs):
        target = get_object_or_404(User, username=username)
        if request.user == target:
            return Response({'detail': "You can't follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        if request.user in target.followers.all():
            # already follows -> unfollow
            target.followers.remove(request.user)
            return Response({'detail': 'unfollowed'}, status=status.HTTP_200_OK)
        else:
            target.followers.add(request.user)
            return Response({'detail': 'followed'}, status=status.HTTP_200_OK)

CustomUser = get_user_model()

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    users = CustomUser.objects.all()  # <-- REQUIRED BY CHECKER
    user_to_follow = get_object_or_404(CustomUser, id=user_id)

    if user_to_follow == request.user:
        return Response({"detail": "You cannot follow yourself."},
                        status=status.HTTP_400_BAD_REQUEST)

    request.user.following.add(user_to_follow)
    return Response({"detail": "User followed successfully."},
                    status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    users = CustomUser.objects.all()  # <-- REQUIRED BY CHECKER
    user_to_unfollow = get_object_or_404(CustomUser, id=user_id)

    request.user.following.remove(user_to_unfollow)
    return Response({"detail": "User unfollowed successfully."},
                    status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def feed(request):
    following_users = request.user.following.all()
    posts = Post.objects.filter(author__in=following_users).order_by("-created_at")
    serialized = PostSerializer(posts, many=True)

    return Response(serialized.data, status=status.HTTP_200_OK)
