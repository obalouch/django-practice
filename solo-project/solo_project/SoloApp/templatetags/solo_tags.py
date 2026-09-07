from django import template
from ..models import Post
from django.db.models import Count


register = template.Library()

@register.simple_tag
def TotalPosts():
    return Post.published.count()

@register.inclusion_tag('solopost/blog/latestpost.html')
def LatestPost(count=5):
    postList = Post.published.order_by('-publish')[:count]
    return {'posts':postList}

@register.simple_tag
def mostComments(count=3):
    mostCP = Post.published.annotate(most_comment = Count('comments')).order_by('-most_comment')[:count]
    return mostCP