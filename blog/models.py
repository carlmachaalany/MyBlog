from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    # so that only the superusers can create the posts
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    # it can be blank because maybe I don't want to publish it yet.(blank=True)
    # maybe I don't have a publication date whatsoever (null=True)
    published_date = models.DateTimeField(blank=True, null=True)

    # This happens when you hit the publish button
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    # This shows all the approved comments of the post
    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    # Here we tell django where should it go after creating a post
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={'pk':self.pk})

    # Just for debugging purposes
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments',on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    # This is to approve a comment
    def approve(self):
        self.approved_comment = True
        self.save()

    # Here we tell django where should it go after creating a comment
    def get_absolute_url(self):
        return reverse("post_list")

    # Just for debugging purposes
    def __str__(self):
        return self.text
