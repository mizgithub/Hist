from django.contrib import admin
from .models import Account, postType,Post, Post_content, saved_posts,graphics,Video_content,Comment, Follows, GenuineBlogers
# Register your models here.
admin.site.register(Account)
admin.site.register(postType)
admin.site.register(Post)
admin.site.register(Post_content)
admin.site.register(saved_posts)
admin.site.register(graphics)
admin.site.register(Video_content)
admin.site.register(Comment)
admin.site.register(Follows)
admin.site.register(GenuineBlogers)