from typing import Any

from django.db.models.query import QuerySet
from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)

from .models import Category, Post, User, Comment
from .forms import UserForm, PostForm, CommentForm
from .consts import PAGINATE_BY
from .mixins import PostMixin, PostsMixin, CommentMixin


class IndexListView(PostsMixin, ListView):
    template_name: str = 'blog/index.html'


class CategoryPostsListView(PostsMixin, ListView):
    template_name: str = 'blog/category.html'

    def get_category(self) -> Category:
        return get_object_or_404(
            Category, slug=self.kwargs['category_slug'], is_published=True
        )

    def get_queryset(self) -> QuerySet[Post]:
        queryset: QuerySet[Post] = super().get_queryset()
        return queryset.filter(
            category=self.get_category(),
            is_published=True,
            pub_date__lte=timezone.now()
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context


class ProfileDetailView(ListView):
    model: type[Post] = Post
    paginate_by: int = PAGINATE_BY
    template_name: str = 'blog/profile.html'
    queryset: QuerySet[Post] = Post.objects.select_related(
        'location', 'author', 'category'
    ).annotate(comment_count=Count('comments')).order_by('-pub_date')

    def get_queryset(self) -> QuerySet[Post]:
        author: User = get_object_or_404(
            User, username=self.kwargs['username']
        )
        if self.request.user == author:
            return self.queryset.filter(author=author)
        return self.queryset.filter(
            author=author, pub_date__lte=timezone.now(), is_published=True
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        author: User = get_object_or_404(
            User, username=self.kwargs['username']
        )
        context['profile'] = author
        return context


class PostDetailView(DetailView):
    model: type[Post] = Post
    template_name: str = 'blog/detail.html'
    queryset: QuerySet[Post] = Post.objects.select_related(
        'location', 'author', 'category'
    )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model: type[User] = User
    form_class = UserForm
    template_name: str = 'blog/user.html'

    def get_object(self) -> User:
        return self.request.user

    def get_success_url(self) -> str:
        return reverse(
            'blog:profile', kwargs={'username': self.object.username}
        )


class PostCreateView(PostMixin, LoginRequiredMixin, CreateView):
    form_class: type[UserForm] = PostForm

    def form_valid(self, form: PostForm) -> Any:
        form.instance.author = self.request.user
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class PostUpdateView(PostMixin, LoginRequiredMixin, UpdateView):
    form_class: type[PostForm] = PostForm

    def dispatch(
            self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        post = get_object_or_404(Post, pk=kwargs['pk'])
        if request.user != post.author:
            return redirect('blog:post_detail', pk=post.pk)
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(PostMixin, LoginRequiredMixin, DeleteView):
    success_url: str = reverse_lazy('blog:index')

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        post: Post = get_object_or_404(Post, pk=kwargs['pk'])
        if request.user != post.author:
            return redirect('blog:index')
        return super().dispatch(request, *args, **kwargs)


class CommentCreateView(LoginRequiredMixin, CreateView):
    target_post = None
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        self.target_post: Post = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: CommentForm) -> HttpResponse:
        form.instance.author: User = self.request.user
        form.instance.post: Post = self.target_post
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('blog:post_detail', kwargs={'pk': self.target_post.pk})


class CommentUpdateView(CommentMixin, LoginRequiredMixin, UpdateView):
    form_class: type[CommentForm] = CommentForm


class CommentDeleteView(CommentMixin, LoginRequiredMixin, DeleteView):
    pass
