from django import forms
from .models import Post, CustomUser, Comment, Hashtag
#from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'location', 'image', 'hashtag_field']

class SigninForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'nickname', 'phone_number', 'password']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class HashtagForm(forms.ModelForm):
    class Meta:
        model = Hashtag
        fields = ['name']