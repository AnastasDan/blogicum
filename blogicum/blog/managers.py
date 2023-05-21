from django.db import models
from django.db.models import Count
from django.utils import timezone


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'location', 'author', 'category'
        ).filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        ).annotate(comment_count=Count('comments')).order_by('-pub_date')
