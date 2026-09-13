from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','email','body']


class EmailForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    to = forms.EmailField()
    reciver = forms.CharField(max_length=20)
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea
    )