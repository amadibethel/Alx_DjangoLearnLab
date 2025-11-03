from relationship_app.models import Author, Book, Library, Librarian

# -----------------------------
# Django ORM Query Samples
# -----------------------------

def get_books_by_author(author_name):
    """
    Returns all books written by a specific author.
    """
    try:
        author = Author.objects.get(name=author_name)
        return Book.objects.filter(author=author)
    except Author.DoesNotExist:
        return []


def get_books_in_library(library_name):
    """
    Returns all books available in a specific library.
    """
    try:
        library = Library.objects.get(name=library_name)
        return library.books.all()
    except Library.DoesNotExist:
        return []


def get_librarian_for_library(library_name):
    """
    Returns the librarian managing a specific library.
    """
    try:
        library = Library.objects.get(name=library_name)
        return library.librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None

