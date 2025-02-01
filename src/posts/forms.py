from django import forms
from django.forms import CheckboxSelectMultiple
from django.forms.models import ModelForm
from .models import Post

class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['url', 'body', 'tags']
        labels = {'url': 'URL', 'body': 'Caption', 'tags': 'Category'}
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a Caption...', 'class': 'font1 text-4xl'}),
            'url': forms.TextInput(attrs={'placeholder': 'Add a URL...'}),
            'tags': CheckboxSelectMultiple(),
        }
class PostEditForm(ModelForm):
    class Meta:
        model = Post
        fields = ['body', 'tags']
        labels = {'body': '', 'tags': 'Category'}
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a Caption...', 'class': 'font1 text-4xl'}),
            'tags': CheckboxSelectMultiple(),
        }
