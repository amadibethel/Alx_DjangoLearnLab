from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


# Serializer for Book model
# Serializes all fields and adds custom validation
class BookSerializer(serializers.ModelSerializer):

    # Custom validation for publication year
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']


# Serializer for Author model
# Demonstrates nested serialization:
# Includes a list of books (BookSerializer) under each Author.
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
