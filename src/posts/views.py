import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PostCreateForm, PostEditForm, CommentCreateForm, ReplyCreateForm
from .models import Post, Tag, Comment, Reply


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
    form = CommentCreateForm()
    reply_form = ReplyCreateForm()
    context = {'post': post, 'form': form, 'reply_form': reply_form}
    return render(request, 'posts/post_page.html', context)


@login_required
def comment_sent(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()
    return redirect('post-page', pk=post.id)

@login_required
def reply_sent(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if request.method == 'POST':
        form = ReplyCreateForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment = comment
            reply.save()
    return redirect('post-page', pk=comment.parent_post.id)


@login_required
def comment_delete_view(request, pk):
    comment = get_object_or_404(Comment, id=pk, author=request.user)
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment Deleted Successfully')
        return redirect('post-page', pk=comment.parent_post.id)
    return render(request, 'posts/comment_delete.html', {'comment': comment})

@login_required
def reply_delete_view(request, pk):
    reply = get_object_or_404(Reply, id=pk, author=request.user)
    if request.method == 'POST':
        reply.delete()
        messages.success(request, 'Reply Deleted Successfully')
        return redirect('post-page', pk=reply.parent_comment.parent_post.id)
    return render(request, 'posts/reply_delete.html', {'reply': reply})

def like_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    user_exists = post.likes.filter(id=request.user.id).exists()

    if post.author != request.user:
        if user_exists:
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
    return redirect('post-page', pk=post.id)