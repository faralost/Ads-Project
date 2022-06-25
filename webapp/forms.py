from django import forms

from webapp.models import Ad, Comment


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        exclude = ('author', 'published_at', 'status',)


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='поиск')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)