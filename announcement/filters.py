import django_filters
from django import forms
from .models import Post


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Название объявления',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    author = django_filters.CharFilter(
        field_name='author__username',
        lookup_expr='icontains',
        label='Имя автора',
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
        fields = ['title', 'author', 'type_post']


