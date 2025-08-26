from django.db.models import Count
from django.shortcuts import get_object_or_404, render, redirect

from accounts.models import CustomUser
from blog.models import Category, Comment, Post
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def index_blog(request):
    posts = Post.objects.filter(is_active=True, main_post=True)[:1]
    random_obj = Post.objects.order_by("?").first()
    random_post = Post.objects.order_by("?")[:4]
    random_trending = Post.objects.filter(is_active=True, section="Trending").order_by(
        "?"
    )[:4]
    random_inspiration = Post.objects.filter(
        is_active=True, category__name="Inspiration"
    ).order_by("?")[:2]
    latest_post = Post.objects.filter(is_active=True).order_by("-created_at")[:3]
    categories_count = Category.objects.annotate(blog_count=Count("post"))

    context = {
        "posts": posts,
        "random_obj": random_obj,
        "random_post": random_post,
        "random_trending": random_trending,
        "random_inspiration": random_inspiration,
        "latest_post": latest_post,
        "categories_count": categories_count,
    }
    return render(request, "blog/index.html", context)


# view to show blog detail
def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post_id=post.id)
    counts_comments = comments.count()
    context = {"post": post, "counts_comments": counts_comments,'comments':comments}

    return render(request, "blog/blog_detail.html", context)


# view to show all blogs in a category
def blog_categories(request, cat):
    cat = Category.objects.get(name=cat, is_active=True)
    blogs_list = Post.objects.filter(is_active=True, category__name=cat)
    paginator = Paginator(blogs_list, 4)  # Show 4 blogs per page
    page = request.GET.get("page", 1)
    try:
        blogs = paginator.get_page(page)
    except EmptyPage:
        blogs = paginator.get_page(paginator.num_pages)
    except PageNotAnInteger:
        blogs = paginator.get_page(1)

    context = {"blogs": blogs, "cat": cat}
    return render(request, "blog/category_blog.html", context)


# view to add comment to a blog post
def add_comment(request, slug):
    if request.user.is_authenticated:
        user = CustomUser.objects.get(email=request.user.email)
        post = get_object_or_404(Post, slug=slug)
        comment_user = Comment.objects.filter(post_id=post.id, user=user).exists()

        if request.method == "POST":
            if comment_user:
                messages.warning(request, "You Already have a comment to this post")
                return redirect("blog:home")
            else:
                subject = request.POST["subject"]
                comment = request.POST["comment"]
                Comment.objects.create(
                    post=post, user=user, subject=subject, body=comment
                )
                messages.success(request, "comment is add success")
                return redirect("blog:blog_detail", post.slug)
        else:
            messages.error(
                request,
                "you are not allowed to comment please create an account register first  or login if you have one",
            )
            return redirect("accounts:login_account")
    else:
        messages.error(request, "you are not authorize please login if you have one")
        return redirect("accounts:login_account")


# view to show all blogs in a section
def blog_section(request, sec):
    blogs_list = Post.objects.filter(is_active=True, section=sec)
    paginator = Paginator(blogs_list, 4)  # Show 4 blogs per page
    page = request.GET.get("page", 1)
    try:
        blogs = paginator.get_page(page)
    except EmptyPage:
        blogs = paginator.get_page(paginator.num_pages)
    except PageNotAnInteger:
        blogs = paginator.get_page(1)

    context = {"blogs": blogs, "section": sec}
    return render(request, "blog/all_post_section.html", context)


# view to show all categories
def all_categories(request):
    categories = Category.objects.filter(is_active=True)
    paginator = Paginator(categories, 4)  # Show 4 blogs per page
    page = request.GET.get("page", 1)
    try:
        categories = paginator.get_page(page)
    except EmptyPage:
        categories = paginator.get_page(paginator.num_pages)
    except PageNotAnInteger:
        categories = paginator.get_page(1)
    context = {"categories": categories}
    return render(request, "blog/all_categories.html", context)


# simple search view
def search_blog(request):
    query = request.GET.get("q")
    if query:
        blogs_list = Post.objects.filter(title__icontains=query, is_active=True)
        context = {"blogs": blogs_list, "query": query}
        return render(request, "blog/all_post_section.html", context)
    else:
        return redirect("blog:home")
