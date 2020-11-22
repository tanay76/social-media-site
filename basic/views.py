from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.views.generic import (View, TemplateView, ListView, DetailView, CreateView,
                                    DeleteView, UpdateView)
from django.contrib.auth.views import PasswordResetView


from .models import *
from .forms import *
#===========================================================================================================================

# Create your views here.
class HomeView(TemplateView):
    template_name = 'index.html'
#===========================================================================================================================

def register(request):
    registered = False
    profile_form = UserProfileInfoForm()
    if request.method == 'POST':
        profile_form = UserProfileInfoForm(request.POST)
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            user = User.objects.filter(Q(username=username)|Q(email=email))
            if user:
                return render(request, 'register.html', {'error':'Username or Email is already taken.'}, {'form':profile_form})
            elif profile_form.is_valid():
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.first_name = firstname
                user.last_name = lastname
                user.set_password(password1)
                user.save()


                profile = profile_form.save(commit=False)
                profile.user = user
                if 'profile_pic' in request.FILES:
                    profile.profile_pic = request.FILES['profile_pic']
                profile.save()
                send_mail(
                    'Subscription',
                    f'You are registered successfully.\nYour Username: { username}.',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False
                )
                registered = True
                return render(request, 'success.html', {'recipient': email})
            else:
                return render(request, 'register.html', {'error':'You are yet to upload your profile image.','form':profile_form})
        else:
            return render(request, 'register.html', {'error':'Passwords mismatch.'}, {'form':profile_form})
    else:
        return render(request, 'register.html', {'form':profile_form})
#================================================================================================================================================

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request,user)
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, 'login.html', {'error':'Invalid Username or Password.'})
    else:
        return render(request, 'login.html')
#=====================================================================================================================

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

#====================================================================================================================================

class Display1(TemplateView):
    template_name = 'display1.html'

#=======================================================================================================================

class UserProfileInfoUpdate(LoginRequiredMixin, UpdateView):
    model = UserProfileInfo
    fields = ['profile_pic']
    template_name = 'propicupdate.html'
    success_url = reverse_lazy('basic:my_profile')



#===========================================================================================================================

class UserDeleteConfirmationView(LoginRequiredMixin, TemplateView):
    template_name = 'confirm_deletion.html'

#===========================================================================================================================

class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('basic:logout')

#===========================================================================================================================

class HomeView(TemplateView):
    template_name = 'index.html'

#===========================================================================================================================

def member_list(request):
    users = User.objects.exclude(is_staff=True)
    return render(request, 'user_list.html', {'users':users})

#===========================================================================================================================

@login_required
def my_profile(request):
    users = User.objects.all()
    for user in users:
        if user == request.user:
            return render(request, 'my_profile.html', {'user':user})

#===========================================================================================================================

def update_user(request, id):
    user = User.objects.get(id=id)
    return render(request, 'user_update.html')

#===========================================================================================================================

def edit_user(request,id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        user.first_name = firstname
        user.last_name = lastname
        user.email = email
        user.save()
        return redirect('basic:my_profile')

#===========================================================================================================================

class PostTopicListView(TemplateView):
    template_name = 'post_topic_list.html'

#===========================================================================================================================

def post_detail(request, pt):
    posts = Post.objects.filter(topic=pt)
    return render(request, 'post_detail_view.html', {'posts':posts})

#===========================================================================================================================

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['topic', 'content', 'video_clips', 'images', 'site_url']
    template_name = 'post_create.html'
    success_url = reverse_lazy('basic:post_topic_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        if 'video_clips' in self.request.FILES:
            form.instance.clips = self.request.FILES['video_clips']
        if 'images' in self.request.FILES:
            form.instance.images = self.request.FILES['images']
        # return super().form_valid(form)
        form.save()
        return HttpResponseRedirect(reverse('basic:post_topic_list'))

#===========================================================================================================================

def post_comment_no(request, id):
    post = get_object_or_404(Post, id=id)
    comments = Comment.objects.filter(post=post)
    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'post_comment_no.html', context)

#===========================================================================================================================

def comment_view(request, id):
    post = get_object_or_404(Post, id=id)
    comments = Comment.objects.filter(post=post)
    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'comment_view.html', context)

#===========================================================================================================================

def reply_view(request, id):
    comment = get_object_or_404(Comment, id=id)
    replies = Comment.objects.filter(reply=comment)
    context = {
        'comment':comment,
        'replies': replies,
    }
    return render(request, 'reply_view.html', context)

#===========================================================================================================================

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content', 'video_clips', 'images', 'site_url']
    template_name = 'comment_create_view.html'

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, id=self.kwargs['id'])
        form.instance.author = self.request.user
        if 'video_clips' in self.request.FILES:
            form.instance.clips = self.request.FILES['video_clips']
        if 'images' in self.request.FILES:
            form.instance.images = self.request.FILES['images']
        # return super().form_valid(form)
        form.save()
        return HttpResponseRedirect(reverse('basic:post_topic_list'))

#===========================================================================================================================

class ReplyCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content', 'video_clips', 'images', 'site_url']
    template_name = 'reply_create_view.html'

    def form_valid(self, form):
        form.instance.reply = get_object_or_404(Comment, id=self.kwargs['id'])
        form.instance.author = self.request.user
        if 'video_clips' in self.request.FILES:
            form.instance.clips = self.request.FILES['video_clips']
        if 'images' in self.request.FILES:
            form.instance.images = self.request.FILES['images']
        # return super().form_valid(form)
        form.save()
        return HttpResponseRedirect(reverse('basic:post_topic_list'))


#===========================================================================================================================


# def already_liked_post(user, id):

#     post= Post.objects.get(id=id)
#     return LikePost.objects.filter(user=user, post=post).exists()

# def post_like_button_clicked(request, id):

#     post = Post.objects.get(id=id)
#     if not already_liked_post(request.user, id):
#         LikePost.objects.create(user=request.user, post=post)
#     else:
#         LikePost.objects.filter(user=request.user, post=post).delete()
#     like_post_count = LikePost.objects.filter(post=post).count()
#     t = TemplateResponse(request, 'post_detail_view', {'likes': like_post_count})
#     t.render()
#     return redirect('basic:post_detail_view', pt='post.topic')

# #===========================================================================================================================

# def already_liked_comment(user, id):

#     comment= Comment.objects.get(id=id)
#     return LikeComment.objects.filter(user=user, post=post).exists()

# def comment_like_button_clicked(request, id):

#     if request.user.is_authenticated():
#         comment = Comment.objects.get(id=id)

#         if not already_liked_comment(request.user, id):
#             LikeComment.objects.create(user=request.user, post=post)
#         else:
#             LikeComment.objects.filter(user=request.user, post=post).delete()
#         like_comment_count = LikeComment.objects.filter(user=request.user, post=post).count()
#         return redirect(reverse())

# #===========================================================================================================================

# def already_disliked_post(user, id):

#     post= Post.objects.get(id=id)
#     return DislikePost.objects.filter(user=user, post=post).exists()

# def post_dislike_button_clicked(request, id):

#     post = Post.objects.get(id=id)
#     import pdb; pdb.set_trace()
#     if not already_disliked_post(request.user, id):
#         DislikePost.objects.create(user=request.user, post=post)
#     else:
#         DislikePost.objects.filter(user=request.user, post=post).delete()
#     dislike_post_count = DislikePost.objects.filter(post=post).count()
#     template = loader.get_template('post_detail_view.html')
#     response_body = template.render({'dislikes':dislike_post_count})
#     return redirect('basic:post_detail_view', pt='post.topic')

# #===========================================================================================================================

# def already_disliked_comment(user, id):

#     comment= Comment.objects.get(id=id)
#     return DislikeComment.objects.filter(user=user, post=post).exists()

# def comment_dislike_button_clicked(request, id):

#     if request.user.is_authenticated():
#         comment = Comment.objects.get(id=id)

#         if not already_disliked_comment(request.user, id):
#             DislikeComment.objects.create(user=request.user, post=post)
#         else:
#             DislikeComment.objects.filter(user=request.user, post=post).delete()
#         dislike_comment_count = DislikeComment.objects.filter(user=request.user, post=post).count()
#         return redirect(reverse('index'))

#===========================================================================================================================

def like_post(request):
    post = get_object_or_404(Post, id=request.POST['post_id'])
    post.like.add(request.user)
    return redirect('basic:post_detail_view', pt=str(post.topic))

def dislike_post(request):
    post = get_object_or_404(Post, id=request.POST['post_id'])
    post.dislike.add(request.user)
    return redirect('basic:post_detail_view', pt=str(post.topic))
#===========================================================================================================================

def like_comment(request):
    comment = get_object_or_404(Comment, id=request.POST['comment_id'])
    comment.like.add(request.user)
    return redirect('basic:reply_view', id=comment.id)

def dislike_comment(request):
    comment = get_object_or_404(Comment, id=request.POST['comment_id'])
    comment.dislike.add(request.user)
    return redirect('basic:reply_view', id=comment.id)

#===========================================================================================================================

def confirm_to_delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    context = {
        'post':post
    }
    return render(request, 'post_confirm_delete.html', context)

class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('basic:post_topic_list')

#===========================================================================================================================

def confirm_to_delete_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    context = {
        'comment':comment
    }
    return render(request, 'comment_confirm_delete.html', context)

class CommentDeleteView(DeleteView):
    model = Comment
    success_url = reverse_lazy('basic:post_topic_list')

#===========================================================================================================================

def confirm_to_delete_reply(request, id):
    reply = get_object_or_404(Comment, id=id)
    context = {
        'reply':reply
    }
    return render(request, 'comment_confirm_delete.html', context)

#======================================================================================================================================


#========================================================================================================================================


#======================================================================================================================================
def view_profile(request, user):
    user1 = User.objects.get(username=user)
    profile = UserProfileInfo.objects.get(user=user1)
    if user1 != request.user:
        context = {
            'user':user1,
            'profile_pic':profile.profile_pic,
        }
    else:
        context = {
            'msg': 'You can view your own profile clicking on My Profile.'
        }
    return render(request, 'profile.html', context)

#============================================================================================================================================

class ProcedureView(TemplateView):
    template_name = 'procedure.html'