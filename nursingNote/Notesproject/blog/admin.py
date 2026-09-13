from django.contrib import admin
from .models import Post , Comment
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','slug','author','created','publish','status']
    list_filter = ['author','publish','status']
    search_fields = ['title','body']
    prepopulated_fields = {
        'slug' : ['title']
    }
    ordering = ['status','-publish']
    date_hierarchy = 'publish'
    show_facets = admin.ShowFacets.ALWAYS
    raw_id_fields = ['author']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name','email','post','created','active']
    list_filter = ['created','active']
    show_facets = admin.ShowFacets.ALWAYS
    