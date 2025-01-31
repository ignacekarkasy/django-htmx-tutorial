from django import forms
from django.forms.models import ModelForm
from django.shortcuts import render, redirect

from .models import Post

def home_view(request, *args, **kwargs):
    posts = Post.objects.all()
    return render(request, 'posts/home.html', {'posts':posts})

class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'body']
        labels = {'title': 'Title', 'image': 'Image', 'body': 'Caption'}
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a Caption...', 'class': 'font1 text-4xl'}),
        }

def post_create_view(request, *args, **kwargs):
    form = PostCreateForm()
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'posts/post_create.html', {'form':form})