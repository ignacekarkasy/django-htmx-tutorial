from django.shortcuts import render
from .models import Post

def home_view(request, *args, **kwargs):
    posts = Post.objects.all()
    return render(request, 'posts/home.html', {'posts':posts})

def post_create_view(request, *args, **kwargs):
    posts = Post.objects.all()
    return render(request, 'posts/post_create.html', {'posts':posts})