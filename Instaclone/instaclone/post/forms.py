from django import forms
from post.models import Post

class Newpostform(forms.ModelForm):
    picture=forms.ImageField(required=True)
    caption=forms.CharField(widget=forms.TextInput(attrs={'class':'input','placeholder':'Caption'}),required=True)
    tag=forms.CharField(widget=forms.TextInput(attrs={'class':'input','placeholder':'tags- Seperate tag with comma'}),required=True)
    class Meta:
        model=Post
        fields=['picture','caption','tag']