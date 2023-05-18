from django import forms
from .models import User, Post, Comment


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author', 'is_published',)
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
