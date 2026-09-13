from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
# Create your models here.

#custome Manager
class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISH)

#table 1 Post    
class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF' , 'Draft'
        PUBLISH = 'PB' , 'Published'

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique_for_date='publish')
    body = models.TextField()

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=2,choices=Status.choices,default=Status.DRAFT)


    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='posts')

    # managers
    objects = models.Manager()
    published = PublishManager()

    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['publish'])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'blog:postDetail',
            args =[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )

class Comment(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    body = models.TextField()
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post,on_delete=models.Case,related_name='comments')

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['created'])]

    def __str__(self):
        return f'by {self.name} at {self.created}'