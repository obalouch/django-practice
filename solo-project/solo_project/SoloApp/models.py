from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.
# declare custome manager :
class PublishManager(models.Manager) :
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISH)
class Post(models.Model):

    #decalre Status
    class Status(models.TextChoices) :
        DRAFT = 'DF' , 'Draft'
        PUBLISH = 'PB' , 'Publish'

    # tables :
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,unique_for_date='publish')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='blog_post')
    status = models.CharField(max_length=2,choices=Status.choices,default=Status.DRAFT)
    tags = TaggableManager()
    # define managers :
    objects = models.Manager() # default
    published = PublishManager() # our custome
    #Meta setting
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'solo:detail' ,
            args=[self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
                ]
        )

class Comment(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created'])]


    def __str__(self):
        return f"commented by {self.name} on {self.post}"

    