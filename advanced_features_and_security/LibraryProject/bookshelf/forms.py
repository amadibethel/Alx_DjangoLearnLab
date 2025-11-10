from django import forms
from .models import Book

# Example form to demonstrate form handling
class ExampleForm(forms.Form):
    name = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(label='Email Address')

# Book form for CRUD
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']

