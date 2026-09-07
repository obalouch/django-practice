from django.contrib import admin
from .models import Post
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','author','status','created','publish','updated']
    list_filter = ['created','publish']
    prepopulated_fields = {
        'slug' : ('title')
    }
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status','publish']
    search_fields = ['title','body']
