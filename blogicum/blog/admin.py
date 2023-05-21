from django.contrib import admin

from .models import Category, Comment, Location, Post

admin.site.empty_value_display = 'Не задано'


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


@admin.display(description='Количество комментариев')
def comment_count(obj):
    return obj.comments.count()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'is_published',
        'author',
        'category',
        'location',
        comment_count,
    )
    list_editable = (
        'is_published',
        'category',
    )
    search_fields = ('title',)
    list_filter = ('is_published',)
    list_display_links = ('title',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
