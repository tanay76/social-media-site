from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.
#===========================================================================================================================

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    profile_pic = models.ImageField(upload_to="profile_pics", blank=True)
    pic_added = models.DateTimeField(auto_now=True)
    pic_updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

#===========================================================================================================================

class Post(models.Model):
    Topic_Choices = [
        ('Science & Tech', 'Science & Tech'),
        ('Politics', 'Politics'),
        ('Economics,Market,Taxes & Investments', 'Economics,Market,Taxes & Investments'),
        ('Literature', 'Literature'),
        ('Art & Culture', 'Art & Culture'),
        ('Law', 'Law'),
        ('Religions', 'Religions'),
        ('Cooking', 'Cooking'),
        ('Food', 'Food Items'),
        ('Fashion & Design', 'Fashion & Design'),
        ('Healthcare,Exercises & Medical', 'Healthcare,Exercises & Medical'),
        ('Games & Sports', 'Games & Sports'),
        ('Jokes', 'Jokes'),
        ('Beauty of Nature', 'Beauty of Nature'),
        ('Others', 'Others')
    ]
    author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    topic = models.CharField(choices=Topic_Choices, max_length=40)
    content = models.TextField(blank=True)
    video_clips = models.FileField(upload_to='videos', blank=True)
    images = models.ImageField(upload_to='images', blank=True)
    site_url = models.URLField(blank=True)
    like = models.ManyToManyField(User, related_name='post_like', blank=True)
    dislike = models.ManyToManyField(User, related_name='post_dislike', blank=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

    def total_likes(self):
        return self.like.count()

    def total_dislikes(self):
        return self.dislike.count()

    # def save(self):
    #     super(Post, self).save()

    # def get_absolute_url(self):
    #     return reverse('comment:post_create', kwargs={'author': self.author})

#===========================================================================================================================

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    reply = models.ForeignKey('Comment', related_name='replies', on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    video_clips = models.FileField(upload_to='videos', blank=True)
    images = models.ImageField(upload_to='images', blank=True)
    site_url = models.URLField(blank=True)
    like = models.ManyToManyField(User, related_name='commment_like', blank=True)
    dislike = models.ManyToManyField(User, related_name='commment_dislike', blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:                     # This helps us to choose anyone among the two fields 'post' & 'reply'
        constraints = [             
            models.CheckConstraint(
                check=Q(post=None) | Q(reply=None),
                name='at_least_1_null'),
        ]

    def __str__(self):
        return self.content

    def total_likes(self):
        return self.like.count()

    def total_dislikes(self):
        return self.dislike.count()


 
#===========================================================================================================================

# class LikePost(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.user.username} likes this post.'

# #===========================================================================================================================

# class LikeComment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.user.username} likes this comment.'

# #===========================================================================================================================

# class DislikePost(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.user.username} dislikes this post.'

#===========================================================================================================================

# class DislikeComment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.user.username} dislikes this comment.'

#===========================================================================================================================
