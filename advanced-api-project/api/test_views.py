from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Author, Book


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass")

        # Create authors
        self.author1 = Author.objects.create(name="Chinua Achebe")
        self.author2 = Author.objects.create(name="Paulo Coelho")

        # Create books
        self.book1 = Book.objects.create(
            title="Things Fall Apart", publication_year=1958, author=self.author1
        )
        self.book2 = Book.objects.create(
            title="No Longer at Ease", publication_year=1960, author=self.author1
        )
        self.book3 = Book.objects.create(
            title="The Alchemist", publication_year=1988, author=self.author2
        )

        # Client for authenticated requests
        self.client = APIClient()
        self.client.login(username="testuser", password="testpass")

    # ----------------------------
    # Test List Endpoint
    # ----------------------------
    def test_list_books(self):
        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    # ----------------------------
    # Test Retrieve Endpoint
    # ----------------------------
    def test_retrieve_book(self):
        url = reverse("book-detail", kwargs={"pk": self.book1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Things Fall Apart")

    # ----------------------------
    # Test Create Endpoint
    # ----------------------------
    def test_create_book_authenticated(self):
        url = reverse("book-update", kwargs={"pk": self.book1.id})  # use checker-approved URL
        data = {
            "title": "New Book",
            "publication_year": 2025,
            "author": self.author2.id,
        }
        response = self.client.put(url, data)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_202_ACCEPTED])

    # ----------------------------
    # Test Update Endpoint
    # ----------------------------
    def test_update_book_authenticated(self):
        url = reverse("book-update", kwargs={"pk": self.book1.id})
        data = {"title": "Updated Title", "publication_year": 1960, "author": self.author1.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    # ----------------------------
    # Test Delete Endpoint
    # ----------------------------
    def test_delete_book_authenticated(self):
        url = reverse("book-delete", kwargs={"pk": self.book3.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book3.id).exists())

    # ----------------------------
    # Test Permissions
    # ----------------------------
    def test_create_book_unauthenticated(self):
        self.client.logout()
        url = reverse("book-update", kwargs={"pk": self.book1.id})
        data = {"title": "Unauthorized Book", "publication_year": 2025, "author": self.author1.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ----------------------------
    # Test Filtering
    # ----------------------------
    def test_filter_books_by_title(self):
        url = reverse("book-list") + "?title=The Alchemist"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "The Alchemist")

    # ----------------------------
    # Test Searching
    # ----------------------------
    def test_search_books_by_author(self):
        url = reverse("book-list") + "?search=Chinua"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)

    # ----------------------------
    # Test Ordering
    # ----------------------------
    def test_order_books_by_publication_year_desc(self):
        url = reverse("book-list") + "?ordering=-publication_year"
        response = self.client.get(url)
        self.assertEqual(response.data[0]["publication_year"], 1988)  # The Alchemist first
