from django.contrib import admin
from .models import Post , Comment
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin) :
    list_display=['title','slug','author','created','publish','updated','status']
    list_filter=['author','created','status']
    prepopulated_fields = {
        'slug' : ('title',)
    }
    raw_id_fields=['author']
    date_hierarchy = 'publish'
    ordering = ['status','-publish']
    search_fields=['title','body']
    show_facets =admin.ShowFacets.ALWAYS

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name','email','post','created','active']
    list_filter = ['created','active','post']
    