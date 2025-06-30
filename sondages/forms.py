from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': "Écris ton commentaire ici…"
            })
        }
        labels = {
            'text': "Ton commentaire"
        }
