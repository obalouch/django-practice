from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = 'solo'
urlpatterns=[
    path('',views.postList,name='post'),
    path('tag/<slug:tag_slug>',views.postList,name='post_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.detail,name='detail'),
    path('<int:post_id>/share',views.sharePost,name='sharePost'),
    path('<int:post_id>/comment',views.CommentPost,name='CommentPost'),
    path('feed',LatestPostsFeed(),name='feed')
]