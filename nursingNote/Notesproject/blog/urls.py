from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('',views.postList,name='posts'),
    path('<int:year>/<int:month>/<int:day>/<slug:postSlug>/',views.postDetail,name='postDetail'),
    path('<int:post_id>/comment',views.commentpost,name='comment')
]
