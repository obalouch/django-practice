from django.shortcuts import render , get_object_or_404
from .models import Post , Comment
from .forms import CommentForm
from django.views.decorators.http import require_POST
# Create your views here.

# all post
def postList(request):
    posts = Post.published.all()
    context = {
        'posts' : posts
    }
    return render(request,'blog/post/posts.html',context)

# post in detail
def postDetail(request,year,month,day,postSlug):
    post = get_object_or_404(
        Post,status = Post.Status.PUBLISH , publish__year = year,
        publish__month = month,
        publish__day = day,
        slug = postSlug
    )
    comments = post.comments.filter(active=True)
    form = CommentForm()

    context = {
        'post' : post,
        'form' : form,
        'comments' : comments
    }
    return render(request,'blog/post/postDetail.html',context)

@require_POST
def commentpost(request,post_id):
    post = get_object_or_404(Post,id=post_id,status = Post.Status.PUBLISH)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
        'form' : form,
        'post' : post,
        'comment' : comment
    }
    return render(request,'blog/post/comment.html',context)