from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.index_blog, name="home"),
    path('blog_detail/<str:slug>/',views.blog_detail,name='blog_detail'),
    path('category/<str:cat>/',views.blog_categories,name='blog_categories'),
    path('comment/<str:slug>/',views.add_comment,name='add_comment')
    ]
