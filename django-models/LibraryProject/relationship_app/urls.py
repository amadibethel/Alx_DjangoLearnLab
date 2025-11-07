from django.urls import path
from . import views

urlpatterns = [
    # ------------------------------
    # Book and Library Views
    # ------------------------------
    path('books/', views.list_books, name='list_books'),  # Function-based view
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),  # Class-based view

    # ------------------------------
    # Authentication Views
    # ------------------------------
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # ------------------------------
    # Role-Based Access Views
    # ------------------------------
    path('admin-view/', views.admin_view, name='admin_view'),
    path('librarian-view/', views.librarian_view, name='librarian_view'),
    path('member-view/', views.member_view, name='member_view'),

    # ------------------------------
    # Book CRUD Views with Permissions
    # ------------------------------
    path('books/add/', views.add_book_view, name='add_book'),
    path('books/edit/<int:pk>/', views.edit_book_view, name='edit_book'),
    path('books/delete/<int:pk>/', views.delete_book_view, name='delete_book'),
]
