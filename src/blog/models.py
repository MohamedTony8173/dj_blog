from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from accounts.models import CustomUser
# from django.urls import reverse
# from django.contrib.auth.models import Permission


# Create your models here.
class Category(models.Model):
    name = models.CharField(_("name"), max_length=50, unique=True)
    slug = models.SlugField(_("slug"), max_length=100, unique=True)
    created_at = models.DateTimeField(_("created at"),   default=timezone.now)
    is_active = models.BooleanField(_("active"),default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


SECTION = (
    ("Popular", "Popular"),
    ("Trending", "Trending"),
    ("Recent", "Recent"),
)


class Post(models.Model):
    title = models.CharField(_("title"), max_length=150, unique=True)
    slug = models.SlugField(_("slug"), unique=True)
    author = models.CharField(_("author"), max_length=50)
    content = models.TextField(_("content"))
    image = models.ImageField(_("image"), upload_to="images/blog")
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    category = models.ForeignKey(
        Category, verbose_name=_("category"), on_delete=models.CASCADE
    )
    section = models.CharField(_("section"), max_length=50, choices=SECTION)
    is_active = models.BooleanField(_("active"),default=True)
    main_post = models.BooleanField(_('main post'),default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        permissions = [
            ("can_publish", "Can publish post"),
        ]
    


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        CustomUser, verbose_name=_("user"), on_delete=models.CASCADE
    )
    subject = models.CharField(_("subject"), max_length=50)
    body = models.TextField(_("body"))
    created_at = models.DateTimeField(_("create at"),  default=timezone.now)
    is_active = models.BooleanField(_("active"),default=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return self.user.first_name

