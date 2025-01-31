import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import PostCreateForm, PostEditForm
from .models import Post


def home_view(request, *args, **kwargs):
    posts = Post.objects.all()
    return render(request, 'posts/home.html', {'posts': posts})


def post_create_view(request, *args, **kwargs):
    form = PostCreateForm()
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            website = form.cleaned_data.get('url')
            response = requests.get(website)
            soup = BeautifulSoup(response.text, 'html.parser')
            find_image = soup.select('meta[content^="https://live.staticflickr.com/"]')
            post.image = find_image[0].get('content')

            find_title = soup.select('h1.photo-title')
            post.title = find_title[0].text.strip()

            find_artist = soup.select('a.owner-name')
            post.artist = find_artist[0].text.strip()

            post.save()
            return redirect('home')
    return render(request, 'posts/post_create.html', {'form': form})


def post_delete_view(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post Deleted Successfully')
        return redirect('home')
    return render(request, 'posts/post_delete.html', {'post': post})


def post_edit_view(request, pk):
    post = Post.objects.get(id=pk)
    form = PostEditForm(instance=post)
    if request.method == 'POST':
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post Edited Successfully')
            return redirect('home')
    context = {'form': form, 'post': post}
    return render(request, 'posts/post_edit.html', context)
