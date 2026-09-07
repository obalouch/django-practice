from django import template
from ..models import Post
from django.db.models import Count
import markdown
from django.utils.safestring import mark_safe





register = template.Library()

@register.simple_tag
def TotalPost():
    return Post.published.count()

@register.inclusion_tag('blog/post/latestPost.html')
def latestPost(count = 5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_Posts':latest_posts}

@register.simple_tag
def get_most_comment(count=5):
    return Post.published.annotate(total_comments = Count('comments')).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_filter(text):
    return mark_safe(markdown.markdown(text))
