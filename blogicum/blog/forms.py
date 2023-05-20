from django import forms
from django.utils import timezone

from .models import User, Post, Comment


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class PostForm(forms.ModelForm):
    pub_date = forms.DateTimeField(
        label='Дата и время публикации',
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M'
        ),
        initial=timezone.now
    )

    class Meta:
        model = Post
        exclude = ('author',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5, 'cols': 50}),
        }
