from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer


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
