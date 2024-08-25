from django import forms
from tinymce.widgets import TinyMCE

from .models import Post, Comment


class PostForm(forms.ModelForm):
    title = forms.CharField(
        label='Название объявления',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    type_post = forms.ChoiceField(
        label='Тип',
        choices=Post.POSITIONS,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    content = forms.CharField(
        label='Содержимое',
        widget=TinyMCE()
    )

    class Meta:
        model = Post
        fields = ['title', 'type_post', 'content']


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        label='Ваш ответ',
        widget=forms.Textarea(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Comment
        fields = ['text']
