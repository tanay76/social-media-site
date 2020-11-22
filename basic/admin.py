from django.contrib import admin
from .models import *

# Register your models here.
class UserProfileInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'pic_added')

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'topic', 'content', 'date')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','post', 'reply', 'author', 'content', 'date')



admin.site.register(UserProfileInfo, UserProfileInfoAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
