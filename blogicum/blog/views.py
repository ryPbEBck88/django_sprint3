from .models import Post, Category
from django.shortcuts import render, get_object_or_404
from django.utils import timezone


def index(request):
    context = {
        'post_list': Post.objects.filter(
            pub_date__lt=timezone.now(),
            is_published=True,
            category__is_published=True,
        ).select_related('category').order_by('-pub_date')[:5]
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )
    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    context = {
        'category': category,
        'post_list': Post.objects.filter(
            category_id=category.id,
            pub_date__lt=timezone.now(),
            is_published=True
        )
    }
    return render(request, 'blog/category.html', context)
