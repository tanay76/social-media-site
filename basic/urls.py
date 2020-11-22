from django.urls import path
from . import views

app_name = 'basic'

urlpatterns = [
    path('register', views.register, name='register'),
    path('user_login',views.user_login,name='user_login'),
    path('logout', views.user_logout, name='logout'),
    path('display1', views.Display1.as_view(), name='display1'),
    path('uploadpropic/<int:pk>', views.UserProfileInfoUpdate.as_view(), name='uploadpropic'),
    path('confirm_deletion/<int:pk>', views.UserDeleteConfirmationView.as_view(), name='confirm_deletion'),
    path('delete/<int:pk>', views.UserDeleteView.as_view(), name='delete'),
    path('member_list', views.member_list, name='member_list'),
    path('my_profile', views.my_profile, name='my_profile'),
    path('view_profile<str:user>', views.view_profile, name='view_profile'),
    path('userupdate/<int:id>', views.update_user, name='userupdate'),
    path('edit_user/<int:id>', views.edit_user, name='edit_user'),
    path('post_topic_list', views.PostTopicListView.as_view(), name='post_topic_list'),
    path('post_detail_view/<str:pt>', views.post_detail, name='post_detail_view'),
    path('post_create/<str:id>', views.PostCreateView.as_view(), name='post_create'),
    path('post_comment_no/<int:id>', views.post_comment_no, name='post_comment_no'),
    path('comment_view/<int:id>', views.comment_view, name='comment_view'),
    path('reply_view/<int:id>', views.reply_view, name='reply_view'),
    path('comment_create_view/<int:id>', views.CommentCreateView.as_view(), name='comment_create_view'),
    path('reply_create_view/<int:id>', views.ReplyCreateView.as_view(), name='reply_create_view'),
    path('like_post', views.like_post, name='like_post'),
    path('dislike_post', views.dislike_post, name='dislike_post'),
    path('like_comment', views.like_comment, name='like_comment'),
    path('dislike_comment', views.dislike_comment, name='dislike_comment'),
    path('confirm_post_deletion_view/<int:id>', views.confirm_to_delete_post, name='confirm_post_deletion_view'),
    path('confirm_comment_deletion_view/<int:id>', views.confirm_to_delete_comment, name='confirm_comment_deletion_view'),
    path('confirm_reply_deletion_view/<int:id>', views.confirm_to_delete_reply, name='confirm_reply_deletion_view'),
    path('delete_post/<int:pk>', views.PostDeleteView.as_view(), name='delete_post'),
    path('delete_comment/<int:pk>', views.CommentDeleteView.as_view(), name='delete_comment'),
    path('procedure', views.ProcedureView.as_view(), name='procedure'),
]