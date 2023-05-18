
from typing import Any, Dict, Type

from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.db.models import Count
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
from django.contrib.auth.decorators import login_required

from .models import Category, Post, User, Comment
from .forms import UserForm, PostForm, CommentForm


class PostsMixin:
    model: Type[Post] = Post
    paginate_by: int = 10
    queryset: QuerySet[Post] = Post.objects.select_related(
        'location', 'author', 'category'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    ).annotate(comment_count=Count('comments')).order_by('-pub_date')


class PostMixin:
    model: Type[Post] = Post
    template_name: str = 'blog/create.html'


class CommentMixin:
    model: Type[Comment] = Comment
    template_name: str = 'blog/comment.html'

    def get_object(self) -> Comment:
        return get_object_or_404(Comment, id=self.kwargs['comment_id'])

    def dispatch(
            self, request: HttpRequest, *args: Any, **kwargs: Any
            ) -> HttpResponse:
        comment: Comment = get_object_or_404(
            Comment, id=self.kwargs['comment_id']
            )
        if comment.author != request.user:
            return redirect('blog:post_detail', pk=comment.post.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        comment: Comment = self.get_object()
        return reverse('blog:post_detail', kwargs={'pk': comment.post.pk})


class IndexListView(PostsMixin, ListView):
    template_name: str = 'blog/index.html'


class CategoryPostsListView(PostsMixin, ListView):
    template_name: str = 'blog/category.html'

    def get_category(self) -> Category:
        return get_object_or_404(
            Category, slug=self.kwargs['category_slug'], is_published=True
        )

    def get_queryset(self) -> QuerySet[Post]:
        return self.get_category().posts.filter(
            is_published=True, pub_date__lte=timezone.now()
        )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context


class ProfileDetailView(ListView):
    model: Type[Post] = Post
    paginate_by: int = 10
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
        else:
            return self.queryset.filter(
                author=author, pub_date__lte=timezone.now(), is_published=True
            )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        author: User = get_object_or_404(
            User, username=self.kwargs['username']
        )
        context['profile'] = author
        return context


class PostDetailView(DetailView):
    model: Type[Post] = Post
    template_name: str = 'blog/detail.html'
    queryset: QuerySet[Post] = Post.objects.select_related(
        'location', 'author', 'category'
    )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model: Type[User] = User
    form_class = UserForm
    template_name: str = 'blog/user.html'

    def get_object(self) -> User:
        return self.request.user

    def get_success_url(self) -> str:
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.object.username}
        )


class PostCreateView(PostMixin, LoginRequiredMixin, CreateView):
    form_class: Type[UserForm] = PostForm

    def form_valid(self, form: PostForm) -> Any:
        form.instance.author = self.request.user
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class PostUpdateView(PostMixin, LoginRequiredMixin, UpdateView):
    form_class: Type[PostForm] = PostForm

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


@login_required
def add_comment(request: HttpRequest, pk: int) -> HttpResponse:
    post: Post = get_object_or_404(Post, pk=pk)
    form: CommentForm = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', pk=pk)


class CommentUpdateView(CommentMixin, LoginRequiredMixin, UpdateView):
    form_class: Type[CommentForm] = CommentForm


class СommentDeleteView(CommentMixin, LoginRequiredMixin, DeleteView):
    pass