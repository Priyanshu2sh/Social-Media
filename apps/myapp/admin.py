from django.contrib import admin
from .models import *

# Register your models here.
class PostsAdmin(admin.ModelAdmin):
    list_display = ('user__email', 'caption', 'location', 'created_at')

admin.site.register(Posts, PostsAdmin)

admin.site.register(PostFiles)
