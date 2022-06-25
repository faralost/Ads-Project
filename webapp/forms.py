from django import forms

from webapp.models import Ad


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        exclude = ('author', 'published_at', 'status',)
