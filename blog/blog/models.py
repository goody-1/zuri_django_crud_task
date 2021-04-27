from django.db import models
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    """Model definition for Post."""

    title = models.CharField(max_length=200, blank=False, null=False)
    author = models.ForeignKey('auth.User', related_name='author', on_delete=models.CASCADE)
    body = models.TextField()


    def __str__(self):
        """Unicode representation of Post."""
        return self.title
        
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    class Meta:
        """Meta definition for Post."""

        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


    