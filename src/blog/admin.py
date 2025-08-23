from django.contrib import admin
from .models import Post, Category, Comment


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active", "created_at"]
    
    prepopulated_fields = {"slug": ("name",)}


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author",'section', "is_active", "created_at",'main_post']
    search_fields = ["title", "author"]
    list_editable = ['main_post',]
    prepopulated_fields = {"slug": ("title",)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "subject", "is_active", "created_at"]
    search_fields = ["is_active", "user"]


admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
