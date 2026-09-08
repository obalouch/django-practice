from django import template
from ..models import Post
from django.db.models import Count
import markdown
from django.utils.safestring import mark_safe

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

@register.filter(name='markdown')
def markdown_filter(text):
    return mark_safe(markdown.markdown(text))