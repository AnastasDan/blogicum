from typing import Any

from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from .consts import PAGINATE_BY
from .models import Comment, Post


class PostsMixin:
    model: type[Post] = Post
    paginate_by: int = PAGINATE_BY

    def get_queryset(self) -> QuerySet[Post]:
        return Post.published.all()


class PostMixin:
    model: type[Post] = Post
    template_name: str = 'blog/create.html'


class CommentMixin:
    model: type[Comment] = Comment
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
