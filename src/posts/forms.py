from django.forms import CheckboxSelectMultiple, Textarea, TextInput
from django.forms.models import ModelForm
from .models import Post

from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):
    # fix to remove default password helptext from signup form
    def __init__(self, *args, **kwargs):
        self.by_passkey = kwargs.pop("by_passkey", False)
        super().__init__(*args, **kwargs)
        if not self.by_passkey:
            self.fields["password1"].help_text = ""


class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['url', 'body', 'tags']
        labels = {'url': 'URL', 'body': 'Caption', 'tags': 'Category'}
        widgets = {
            'body': Textarea(attrs={'rows': 3, 'placeholder': 'Add a Caption...', 'class': 'font1 text-4xl'}),
            'url': TextInput(attrs={'placeholder': 'Add a URL...'}),
            'tags': CheckboxSelectMultiple(),
        }

class PostEditForm(ModelForm):
    class Meta:
        model = Post
        fields = ['body', 'tags']
        labels = {'body': '', 'tags': 'Category'}
        widgets = {
            'body': Textarea(attrs={'rows': 3, 'placeholder': 'Add a Caption...', 'class': 'font1 text-4xl'}),
            'tags': CheckboxSelectMultiple(),
        }
