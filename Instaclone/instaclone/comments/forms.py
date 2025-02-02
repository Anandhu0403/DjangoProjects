from django import forms
from comments.models import Comments

class Commentform(forms.ModelForm):
    body=forms.CharField(widget=forms.TextInput(attrs={'class':'input','placeholder':'Enter comment'}),required=True)
    class Meta:
        model=Comments
        fields=['body']