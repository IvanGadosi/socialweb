from django.db import models
from datetime import datetime
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver

from accounts.models import CustomUser
from categories.models import Category

class Post(models.Model):
    post_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    date_created=models.DateTimeField(default=datetime.now, blank=True, editable=False)
    description=models.TextField(blank=True,null=True)
    category=models.ForeignKey(Category, blank=True,null=True, on_delete=models.CASCADE)
    post_image=models.ImageField(upload_to='post_images/', blank=True, null=True)
    rating=models.IntegerField(default=0)
    creator=models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Voter(models.Model):
    voter_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    voter_post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Comment(models.Model):
    comment_id=models.AutoField(primary_key=True)
    comment_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateTimeField(default=datetime.now, blank=True, editable=False)

    class Meta:
        ordering = ['-comment_date']

    def __str__(self):
        return 'Comment {} by {}'.format(self.comment_id, self.comment_user)

@receiver(post_delete, sender=Post)
def media_delete(sender, instance, **kwargs):
    instance.post_image.delete(False)

@receiver(post_delete, sender=CustomUser)
def media_delete(sender, instance, **kwargs):
    instance.user_image.delete(False)