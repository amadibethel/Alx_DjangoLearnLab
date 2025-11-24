from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework
from django_filters import rest_framework as filters


# ListView — GET /books/
# Purpose: Retrieve ALL Book objects.
# Accessible by anyone (AllowAny).
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# DetailView — GET /books/<id>/
# Purpose: Retrieve a single Book by ID.
# Accessible by anyone (AllowAny).
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticatedOrReadOnly]
    


# CreateView — POST /books/create/
# Purpose: Create a new Book.
# Restricted to authenticated users only.
# Custom validation handled by BookSerializer.
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Example of custom behavior: automatically check request user before saving
    def perform_create(self, serializer):
        # This hook allows adding extra logic before saving.
        serializer.save()


# UpdateView — PUT/PATCH /books/<id>/update/
# Purpose: Update an existing Book.
# Restricted to authenticated users only.
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # Additional custom hook example
        serializer.save()


# DeleteView — DELETE /books/<id>/delete/
# Purpose: Delete a Book.
# Restricted to authenticated users only.
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Enable filtering, searching, ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Filtering
    filterset_fields = ["title", "author", "publication_year"]

    # Search
    search_fields = ["title", "author"]

    # Ordering
    ordering_fields = ["title", "publication_year"]
    ordering = ["title"]


class BookDetailView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookUpdateView(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]   # Protected route


class BookDeleteView(DestroyAPIView):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]   # Protected route

class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Filtering, Searching, Ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Filtering fields
    filterset_fields = ["title", "author", "publication_year"]

    # Search fields
    search_fields = ["title", "author"]

    # Ordering fields
    ordering_fields = ["title", "publication_year"]
    ordering = ["title"]