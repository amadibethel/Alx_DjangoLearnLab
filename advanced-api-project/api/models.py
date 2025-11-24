from django.db import models

# Author model
# Stores basic information about a writer.
# One author can have multiple books (1-to-many relationship).
class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Book model
# Stores info about a book written by an Author.
# Linked to Author through a ForeignKey (Many books → One author).
class Book(models.Model):
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
