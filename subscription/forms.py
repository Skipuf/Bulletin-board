from django import forms
from tinymce.widgets import TinyMCE

from .models import SubscriptionMessages


class CreateSubscription(forms.ModelForm):
    title = forms.CharField(
        label='Заголовок письма',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    text = forms.CharField(
        label='Содержимое',
        widget=forms.Textarea(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = SubscriptionMessages
        fields = ['title', 'text']
