from django.shortcuts import render , get_object_or_404
from .models import Post 
from .forms import CommentForm , EmailForm
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
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

def share(request,post_id):
    post = get_object_or_404(Post,id = post_id)

    sent = False
    form = EmailForm(data=request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        postUrl = request.build_absolute_uri(post.get_absolute_url())
        subject = (
            f"{cd['name']} has recommended {post.title} to you"
        )
        message = (
            f"Dear {cd['reciver']} You can read '{post.title}' at {postUrl}\n+"
            f"{cd['name']} also commented {cd['comment']}"
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=None,
            recipient_list=[cd['to']]
        )
        sent = True
    context = {
        'sent' : sent,
        'post' : post,
        'form' : form
    }
    return render(request,'blog/post/share.html',context)
