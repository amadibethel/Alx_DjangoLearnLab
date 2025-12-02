from django import forms
from .models import Post
from .models import Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from .models import Post, Comment, Profile, Tag
from taggit.forms import TagWidget

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email")

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "avatar")

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...'}),
        max_length=2000
    )

    class Meta:
        model = Comment
        fields = ['content']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email")


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "profile_picture")


class PostForm(forms.ModelForm):
    # Accept tags as a comma-separated string for simple UX
    tags = forms.CharField(
        required=False,
        help_text="Comma-separated list of tags. Example: django, tips, tutorial"
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

    def clean_tags(self):
        raw = self.cleaned_data.get('tags', '')
        # normalize: split by comma and strip whitespace, ignore empty
        tags = [t.strip() for t in raw.split(',') if t.strip()]
        # de-duplicate preserving order
        seen = set()
        unique = []
        for t in tags:
            low = t.lower()
            if low not in seen:
                seen.add(low)
                unique.append(t)
        return unique

    def save(self, commit=True, user=None):
        """
        save() will handle tags separately; pass user when creating to set author if desired.
        """
        tags_list = self.cleaned_data.pop('tags', [])
        post = super().save(commit=commit)
        # attach tags (create if not exists)
        if commit:
            post.tags.clear()
            for tag_name in tags_list:
                tag_obj, _ = Tag.objects.get_or_create(name=tag_name)
                post.tags.add(tag_obj)
        else:
            # if not commit, tags will be attached after post.save() externally
            self._pending_tags = tags_list
        return post


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...'}),
        max_length=2000
    )

    class Meta:
        model = Comment
        fields = ['content']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'tags']
        widgets = {
            'tags': TagWidget(),
        }
