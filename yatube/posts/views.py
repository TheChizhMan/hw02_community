from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from .models import Group, Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import PostForm


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, settings.PAGE_SIZE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, settings.PAGE_SIZE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username: str):
    user = User.objects.get(username=username)
    post_list = user.posts.all()
    paginator = Paginator(post_list, settings.PAGE_SIZE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'user': user,
        'page_obj': page_obj,
        'post_count': user.posts.count()}
    # Выводим шаблон с данными
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id: int):
    post = get_object_or_404(Post, pk=post_id)
    post_list = post.author.posts.count()
    context = {
        'post': post,
        'post_count': post_list,
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', username=request.user.username)
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('post_detail', post_id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/update_post.html',
                  {'form': form, 'is_edit': True})
