from django.shortcuts import render , get_object_or_404
from .models import Post , Comment
from django.views.generic import ListView
from .forms import EmailForm , CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator , EmptyPage , InvalidPage
from taggit.models import Tag
from django.db.models import Count
# Create your views here.

def postList(request,tag_slug = None) :
    post_list = Post.published.all()
    tag = None
    if tag_slug :
        tag = get_object_or_404(Tag,slug = tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list,3)
    page_number = request.GET.get('page',1) 
    try :   
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except InvalidPage:
        posts = paginator.page(1)

    context = {
        'posts' : posts,
        'tag' : tag
    }

    return render(request,'solopost/blog/post/posts.html',context)




def detail(request,year,month,day,post):
    post = get_object_or_404(Post,status = Post.Status.PUBLISH,publish__year=year,publish__month=month,publish__day=day,slug=post)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    post_tag_id = post.tags.values_list('id',flat=True)
    similar_posts = None
    similar_posts = Post.published.filter(tags__in=post_tag_id).exclude(id=post.id)
    if similar_posts :
         similar_posts = similar_posts.annotate(same_tags = Count('tags')).order_by('same_tags','-publish')
    context = {
        'post' : post,
        'form' : form,
        'comments' : comments,
        'similar_post' : similar_posts
    }
    return render(request,'solopost/blog/post/detail.html',context)

def sharePost(request,post_id):
    post = get_object_or_404(Post,id = post_id,status = Post.Status.PUBLISH)
    sent = False
    if request.method == 'POST' :
        form = EmailForm(data=request.POST)
        if form.is_valid():
            mail = form.cleaned_data
            postUrl = request.build_absolute_uri(post.get_absolute_url())
            subject = (f"{mail['name']} has recommended to read {post.title}")
            message = (f"read {post.title} at {postUrl}"
                       f"{mail['name']} comment {mail['comments']}")
            send_mail(subject=subject,message=message,from_email=None,recipient_list=[mail['to']])
            sent = True
    else:
        form = EmailForm()

    context = {
                'post':post,
                'form':form,
                'sent' : sent
            }
    return render(request,'solopost/blog/post/share.html',context)


@require_POST
def CommentPost(request,post_id) :
    post = get_object_or_404(Post,id = post_id,status = Post.Status.PUBLISH)
    form = CommentForm(data=request.POST)
    comment = None
    if form.is_valid():
        comment  = form.save(commit=False)
        comment.post = post
        comment.save()

    context = {
        'post' : post,
        'form' : form,
        'comment' : comment
    }
    return render(request,'solopost/blog/post/comment.html',context)