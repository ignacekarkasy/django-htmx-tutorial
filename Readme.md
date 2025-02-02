# Readme

# Notes

## Django

### Database field relations
- 1:1 relations
  - Requires target model in defining model
  - Can set cascading
- 1:n relations
  - Requires target model name as string
- foreign_key relations
```python
from django.db import models
from django.contrib.auth.models import User
models.OneToOneField(User, on_delete=models.CASCADE)
tags = models.ManyToManyField('Tag')
```
[rel 1:1](https://youtu.be/jGHmbpaix7k?list=PL5E1F5cTSTtTAIw_lBp1hE8nAKfCXgUpW&t=352),
[rel 1:1n](https://youtu.be/dhSVKFgkL5M?list=PL5E1F5cTSTtTAIw_lBp1hE8nAKfCXgUpW&t=40)
[rel foreign](https://youtu.be/8eD7NyMZdg8?list=PL5E1F5cTSTtTAIw_lBp1hE8nAKfCXgUpW&t=72)
### Model definition parameters
```python
from django.db import models
realname = models.CharField(max_length=20, null=True, blank=True)
```
- `null=True`: Field is nullable or not (Database)
- `blank=True`: Field is optional or not (Forms)

[rel](https://youtu.be/jGHmbpaix7k?list=PL5E1F5cTSTtTAIw_lBp1hE8nAKfCXgUpW&t=479)
### Database cascading on delete

For cascading deletion of the ORM `on_delete=models.CASCADE` can be set in relation definition.
The non cascading property is used via `on_delete=models.SET_NULL`.
```python
from django.db import models
from django.contrib.auth.models import User
user = models.OneToOneField(User, on_delete=models.CASCADE)
author = models.ForeignKey(User, on_delete=models.SET_NULL)
```
[rel SET_NULL](https://youtu.be/8eD7NyMZdg8?list=PL5E1F5cTSTtTAIw_lBp1hE8nAKfCXgUpW&t=97)
[rel CASCADE](https://youtu.be/jGHmbpaix7k?list=PL5E1F5cTSTtTAIw_lBp1hE8nAKfCXgUpW&t=401)

### Magic

here `related_name='posts'` will create a new field in `User` to keep relations of users<->posts.
```python
author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posts')
```
### Filter form fields models
- `exclude` excludes fields with `['user']`
- `fields` includes sppecified list with `['image', 'realname', 'email', 'location', 'bio']`

```python
class ProfileEditFormExclude(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

class ProfileEditFormInclude(ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'realname', 'email', 'location', 'bio']
        fields = __all__
```
[rel exclude](https://youtu.be/jGHmbpaix7k?list=PL5E1F5cTSTtTAIw_lBp1hE8nAKfCXgUpW&t=1293)

### FileInput widget for file uploads
This replaces the Admin style render for the image with a default one in forms via widget.
```python
from django.forms.models import ModelForm
from django.forms import FileInput

class ExampleForm(ModelForm):
    class Meta:
        widgets = {
            'image': FileInput(),
        }
```
[rel](https://youtu.be/jGHmbpaix7k?list=PL5E1F5cTSTtTAIw_lBp1hE8nAKfCXgUpW&t=1333)

### Handle image form posts
The `request.FILES` property needs to be passed to the form.
```python
form = SomeForm(request.POST, request.FILES, instance=request.user.profile)
```
[rel](https://youtu.be/jGHmbpaix7k?list=PL5E1F5cTSTtTAIw_lBp1hE8nAKfCXgUpW&t=1409)
## Hurdles

### Form field select with \_\_all__ does not work
Using `fields = __all__` results in an undefined error. 
```python
    fields = __all__
             ^^^^^^^
NameError: name '__all__' is not defined. Did you mean: '__name__'?
```
[rel include all](https://youtu.be/eXFMz0QRNDY?list=PL5E1F5cTSTtTAIw_lBp1hE8nAKfCXgUpW&t=1455)

### UUID as post primary key

The suggested method of defining this in the Post model failed.
This was the solution for this hurdle:
```python
from django.db import models
import uuid
id = models.UUIDField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
```
[rel](https://youtu.be/eXFMz0QRNDY?list=PL5E1F5cTSTtTAIw_lBp1hE8nAKfCXgUpW&t=343)
### AllAuth changed their template structure

There is no `base.html` anymore, AllAuth introduced layouts as well, 
which can be found in `allauth/templates/allauth/layouts/base.html` and needed to be duplicated as well.

[rel](https://youtu.be/gamULNTZsMM?list=PL5E1F5cTSTtTAIw_lBp1hE8nAKfCXgUpW&t=677)
### AllAuth changed the signup form

The  signup form always displayed the password requirement hints, which didnt align with the tutorial.
By introducing a signup override in `settings.py` the `CustomSignupForm` form is used in `posts/forms.py`, 
extending the default and removing the hint.

```python
ACCOUNT_FORMS = {
    'signup': 'posts.forms.CustomSignupForm',  # replace default signup form on signup, to remove password hints help.
}
```
```python
from allauth.account.forms import SignupForm
class CustomSignupForm(SignupForm):
    # fix to remove default password helptext from signup form
    def __init__(self, *args, **kwargs):
        self.by_passkey = kwargs.pop("by_passkey", False)
        super().__init__(*args, **kwargs)
        if not self.by_passkey:
            self.fields["password1"].help_text = ""

```
[rel](https://youtu.be/gamULNTZsMM?list=PL5E1F5cTSTtTAIw_lBp1hE8nAKfCXgUpW&t=768)
### AllAuth redirect urls not working
First i needed to adapt to AllAuths changes since the recording of the tutorial. 
The access to the redirect property has changed, which i managed to access via AllAuth's adapters.

I needed to overwrite AllAuths adapter `ACCOUNT_ADAPTER` and created a extension in `users/adapters.py`.
Here i extend from `from allauth.account.adapter import DefaultAccountAdapter` whose 2 redirect methods are overloaded.
- `get_login_redirect_url()`
- `get_signup_redirect_url()`

There is basically no change, but without this adapter the settings `SIGNUP_REDIRECT_URL` and `LOGIN_REDIRECT_URL`
dont seem to work.

[rel](https://youtu.be/GBOmZRfBR-g?list=PL5E1F5cTSTtTAIw_lBp1hE8nAKfCXgUpW&t=889)
### Django forms render produced extra wrapper div
Without styling the div maintains the width of the child.
adding a tailwind class with `w-full` just to the input would have no effect since as a child is already using 100%.
I found no quick/easy way to configure the formclass to add a class to its wrapper.
As a workaround i iterate over the fields and print them individually.
This way no form wrapper div is applied.

[rel](https://youtu.be/T5Jfb_LkoV0?list=PL5E1F5cTSTtTAIw_lBp1hE8nAKfCXgUpW&t=665)
## Tutorial feedback
- in all class `__str__` casts, a `str()` cast is not necessary, because the objets/fields are known.
- shows something that is out of order [1](https://www.youtube.com/watch?v=8eD7NyMZdg8&lc=UgxdwJ4u0-KA3Q83OhZ4AaABAg)