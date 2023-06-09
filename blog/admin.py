from django.contrib import admin

# Register your models here.
from blog.models import Post

# admin.site.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display=["title","timestamp"]
    list_display_links=["timestamp"]
    list_editable=["title"]
    list_filter=["timestamp"]
    search_fields=["title","content"]
    class Meta:
        model=Post
admin.site.register(Post,PostModelAdmin)