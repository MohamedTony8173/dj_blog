
from blog.models import Category, Post


def popular(request):
    return  {'popular' : Post.objects.filter(is_active=True,section='Popular').order_by('-created_at')[:5]}

def recent(request):
    return {'recent': Post.objects.filter(is_active=True,section='Recent').order_by('-created_at')[:5]}

def categories(request):
    return { 'categories' : Category.objects.filter(is_active=True)}
    