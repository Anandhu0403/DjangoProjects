from django.contrib import admin

# Register your models here.
from post.models import Tag,Post,Follow,Stream
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Stream)