from django.shortcuts import render , get_object_or_404
from django.http import Http404
from .models import Post
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm ,CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
# Create your views here.

def post_list(request,tag_slug = None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag , slug = tag_slug)
        post_list = post_list.filter(tags__in = [tag])
    paginator = Paginator(post_list,3)
    page_number = request.GET.get('page',1)
    try :
        posts =paginator.page(page_number) 
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger :
        posts = paginator.page(1)
    context = {
        'posts' : posts,
        'tag' : tag,
    }
    return render(request,'blog/post/list.html',context) # function base view
# class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_share(request,post_id):
    post = get_object_or_404(Post,id = post_id,status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST' :
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (f"{cd['name']} ({cd['email']}) has recommended to read {post.title} ")
            message = (
                f"read {post.title} at {post_url}\n\n"
                f"{cd['name']} comments : {cd['comments']}"
                )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            sent = True
    else :
        form = EmailPostForm()

    context = {
        'post' : post,
        'form' : form,
        'sent' : sent
    }
    return render(request,'blog/post/share.html',context)
    
def post_detail(request,year,month,day,post) :

    # try :
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404("Page Not Find")
    post = get_object_or_404(Post,status=Post.Status.PUBLISHED,publish__year=year,publish__month=month,publish__day=day,slug=post)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    post_tag_id = post.tags.values_list('id',flat=True)
    same_post = Post.published.filter(tags__in = post_tag_id).exclude(id=post.id)
    same_post = same_post.annotate(same_tags = Count('tags')).order_by('-same_tags','-publish')[:4]
    context = {
        'post' : post,
        'comments' : comments,
        'form' : form,
        'similar_posts' : same_post,
    }

    return render(request,'blog/post/detail.html',context)

@require_POST
def comment_post(request,post_id):
    post = get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
        'post' : post,
        'form' : form,
        'comment' : comment
    }
    return render(request,'blog/post/comment.html',context)