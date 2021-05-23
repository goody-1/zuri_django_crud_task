from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    """Model definition for Post."""

    title = models.CharField(max_length=200, blank=False, null=False)
    author = models.ForeignKey('auth.User', related_name='author', on_delete=models.CASCADE)
    body = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        """Unicode representation of Post."""
        return self.title
        
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    class Meta:
        """Meta definition for Post."""

        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


    