import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PostCreateForm, PostEditForm
from .models import Post, Tag


def home_view(request, tag=None, *args, **kwargs):
    if tag:
        posts = Post.objects.filter(tags__slug=tag)
        tag = get_object_or_404(Tag, slug=tag)
    else:
        posts = Post.objects.all()

    categories = Tag.objects.all()
    return render(request, 'posts/home.html', {'posts': posts, 'categories': categories, 'tag': tag})


@login_required
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

            post.author = request.user

            post.save()
            form.save_m2m()
            return redirect('home')
    return render(request, 'posts/post_create.html', {'form': form})


@login_required
def post_delete_view(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post Deleted Successfully')
        return redirect('home')
    return render(request, 'posts/post_delete.html', {'post': post})


@login_required
def post_edit_view(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    form = PostEditForm(instance=post)
    if request.method == 'POST':
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post Edited Successfully')
            return redirect('home')
    context = {'form': form, 'post': post}
    return render(request, 'posts/post_edit.html', context)


def post_page_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/post_page.html', {'post': post})
