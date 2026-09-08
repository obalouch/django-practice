import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post

class LatestPostsFeed(Feed):
    title = 'My Blog'
    link = reverse_lazy('solo:post')
    description = 'solo Feed'

    def items(self):
        return Post.published.all()[:5]

    def item_pubdate(self,item):
        return item.publish

    def item_descriptin(self,item):
        return truncatewords_html(markdown.markdown(item.body),30)