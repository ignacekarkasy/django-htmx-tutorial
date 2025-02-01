from django.forms import CheckboxSelectMultiple, Textarea, TextInput, FileInput
from django.forms.models import ModelForm
from .models import Profile

class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        labels = {
            'realname': 'Name'
        }
        widgets = {
            'image': FileInput(),
            'bio': Textarea(attrs={'rows': 3}),
        }
