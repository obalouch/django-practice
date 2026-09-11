from django.shortcuts import render
from .models import Post
# Create your views here.

# all post
def postList(request):
    posts = Post.published.all()
    context = {
        'posts' : posts
    }
    return render(request,'blog/posts.html',context)