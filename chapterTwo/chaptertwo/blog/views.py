from django.shortcuts import render
from .models import Post
from django.views.generic import ListView
# Create your views here.

class PostList(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'blog/post/postlist.html'
