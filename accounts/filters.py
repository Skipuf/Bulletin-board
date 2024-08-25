import django_filters
from django import forms
from announcement.models import Comment, Post


class CommentsFilter(django_filters.FilterSet):
    post__title = django_filters.CharFilter(
        field_name='post__title',
        lookup_expr='icontains',
        label='Название поста',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Comment
        fields = ['post__title']


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Название объявления',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    type_post = django_filters.ChoiceFilter(
        field_name='type_post',
        label='Тип',
        choices=Post.POSITIONS,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = Post
        fields = ['title', 'type_post']



