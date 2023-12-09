from pyexpat import model
from sqlite3 import Timestamp
from django.db import models
from dashboard.models import Article
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Articles(models.Model):
    title = models.CharField(max_length=200)
    img_title = models.CharField(max_length=200)  # Assuming it's a CharField, adjust if needed
    slug = models.SlugField(unique=True)
    img_alt = models.CharField(max_length=200)  # Assuming it's a CharField, adjust if needed
    tags = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to='Article/thumbnails/')
    short_description = models.TextField()
    main_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    email_token=models.CharField(max_length=200)
    is_verified=models.BooleanField(default=False)
    token_expires_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"Profile of {self.user.username}"
    
class Comment(models.Model):
    sno = models.AutoField(primary_key=True)
    post_title = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post_title.title}"
    
class Contactus(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    massage =  models.TextField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.name

