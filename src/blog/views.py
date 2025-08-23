from django.db.models import Count
from django.shortcuts import get_object_or_404, render, redirect

from accounts.models import CustomUser
from blog.models import Category, Comment, Post
from django.contrib import messages


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


def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post_id=post.id)
    counts_comments = comments.count()
    context = {"post": post, "counts_comments": counts_comments}

    return render(request, "blog/blog_detail.html", context)


def blog_categories(request, cat):
    cat = Category.objects.get(name=cat, is_active=True)
    blogs = Post.objects.filter(is_active=True, category__name=cat)
    context = {"blogs": blogs, "cat": cat}
    return render(request, "blog/category_blog.html", context)


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
