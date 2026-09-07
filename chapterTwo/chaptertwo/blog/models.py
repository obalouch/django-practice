from django.db import models
from django.utils import timezone
from django.conf import settings
# Create your models here.

class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = Post.Status.PUBLISH)
class Post(models.Model) :

    class Status(models.TextChoices):
        DRAFT = 'DF' , 'Draft'
        PUBLISH = 'PB' , 'Publish'
    # text
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    body = models.TextField()

    # time
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(default=timezone.now())

    # authentication
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='posts')

    # status
    status = models.CharField(max_length=2,choices=Status.choices , default=Status.DRAFT)

    # manager
    objects = models.Manager() #default manager
    published = PublishManager()



    # absolute url




    # Meta setting
    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['publish'])]


    def __str__(self):
        return self.title
