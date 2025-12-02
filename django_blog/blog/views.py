from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Comment, Post
from .forms import CommentForm
from .models import Post, Tag, Comment
from django.views.generic import ListView
from taggit.models import Tag
from .forms import PostForm, CommentForm, CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm


from .forms import (
    CustomUserCreationForm,
    UserUpdateForm,
    ProfileUpdateForm,
    PostForm
)
from .models import Post


# -------------------------------------------------------------------
# Authentication & Profile Views
# -------------------------------------------------------------------

def register(request):
    """User registration"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                f"Account created for {user.username}. You can now log in."
            )
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'blog/register.html', {'form': form})


@login_required
def profile(request):
    """View + Update logged-in user profile"""

    if request.method == 'POST':
        u_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )
        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'blog/profile.html', {
        'u_form': u_form,
        'p_form': p_form
    })


def index(request):
    """Homepage view"""
    return render(request, 'blog/index.html')


# -------------------------------------------------------------------
# Blog CRUD Views (Class-Based Views)
# -------------------------------------------------------------------

class PostListView(ListView):
    """Display all posts"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5


class PostDetailView(DetailView):
    """View a single post"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    """Create a new post (must be logged in)"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user  # auto-assign author
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update a post — only if user is author"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        return self.request.user == self.get_object().author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a post — only if user is author"""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):
        return self.request.user == self.get_object().author

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'  # used when not embedding inline

    def form_valid(self, form):
        # post_id from URL kwargs
        post_pk = self.kwargs.get('post_pk')
        post = get_object_or_404(Post, pk=post_pk)
        form.instance.post = post
        form.instance.author = self.request.user
        response = super().form_valid(form)
        # redirect back to the post detail page
        return redirect('blog:post_detail', pk=post.pk)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['post'] = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        return ctx


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        return self.request.user == self.get_object().author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        return self.request.user == self.get_object().author

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comment_form'] = CommentForm()
        return ctx

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comment_form'] = CommentForm()
        return ctx


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        # set author and save post then handle tags created in form.save()
        form.instance.author = self.request.user
        post = form.save(commit=False)
        post.save()
        # attach tags if creation left them pending
        if hasattr(form, '_pending_tags'):
            for tag_name in form._pending_tags:
                tag_obj, _ = Tag.objects.get_or_create(name=tag_name)
                post.tags.add(tag_obj)
        else:
            # if PostForm saved tags already, nothing to do
            pass
        return redirect(post.get_absolute_url())


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def get_initial(self):
        initial = super().get_initial()
        # pre-fill tags field with comma-separated tags
        initial_tags = ', '.join([t.name for t in self.get_object().tags.all()])
        initial['tags'] = initial_tags
        return initial

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        # attach/update tags (PostForm.save handles when commit=True)
        if hasattr(form, '_pending_tags'):
            post.tags.clear()
            for tag_name in form._pending_tags:
                tag_obj, _ = Tag.objects.get_or_create(name=tag_name)
                post.tags.add(tag_obj)
        return redirect(post.get_absolute_url())

    def test_func(self):
        return self.request.user == self.get_object().author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):
        return self.request.user == self.get_object().author


# -----------------------
# Tag views
# -----------------------
class PostsByTagView(ListView):
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        tag_name = self.kwargs.get('tag_name')
        return Post.objects.filter(tags__name__iexact=tag_name).distinct().order_by('-published_date')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['tag_name'] = self.kwargs.get('tag_name')
        return ctx


# -----------------------
# Search view
# -----------------------
class SearchResultsView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if not query:
            return Post.objects.none()
        # search title, content and tag names (case-insensitive)
        return Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct().order_by('-published_date')
Notes:

PostCreateView and PostUpdateView now handle tags (creating Tag rows if needed).

PostsByTagView lists posts for a tag name.

SearchResultsView uses Q to search title, content and tag names.

4) blog/urls.py — add tag & search routes + confirm correct post routes
Replace or update your blog/urls.py with:

python
Copy code
from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    # Post routes
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    # Comments (ensure these views exist if you implemented them)
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),

    # Tags & search
    path('tags/<str:tag_name>/', views.PostsByTagView.as_view(), name='posts_by_tag'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
]

def post_list(request):
    query = request.GET.get('q')
    posts = Post.objects.all()

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query)
        )
    
    return render(request, 'blog/post_list.html', {'posts': posts}

class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        return Post.objects.filter(tags__slug=tag_slug)