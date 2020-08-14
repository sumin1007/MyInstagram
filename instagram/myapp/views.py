from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, CustomUser, Hashtag
from .forms import PostForm, SigninForm, UserForm, CommentForm, HashtagForm

#from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpResponse

# Create your views here.
def layout(request):
    return render(request, 'myapp/layout.html')

def home(request):
    posts = Post.objects
    comment_form = CommentForm()
    return render(request, 'myapp/home.html', {'posts':posts, 'comment_form': comment_form})

def post(request):
    if not request.user.is_active:
        return HttpResponse("Can't write a post without Sign In")
    
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            posts = form.save(commit=False)
            posts.writer = request.user

            hashtag_field = form.cleaned_data['hashtag_field']
            str_hashtags = hashtag_field.split('#')
            list_hashtags = list()

            for hashtag in str_hashtags:
                if Hashtag.objects.filter(name=hashtag):
                    list_hashtags.append(Hashtag.objects.get(name=hashtag))
                else:
                    temp_hashtag = HashtagForm().save(commit=False)
                    temp_hashtag.name = hashtag
                    temp_hashtag.save()
                    list_hashtags.append(temp_hashtag)

            posts.save()
            posts.hashtags.add(*list_hashtags)
            
            return redirect('home')
    else:
        form = PostForm()
        return render(request, 'myapp/post.html', {'form':form})

def read(request):
    return redirect('home')

def update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)
        return render(request, 'myapp/post.html', {'form':form})

def delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('home')

def start(request):
    signin_form = SigninForm()
    return render(request, 'myapp/start.html', {'signin_form': signin_form})

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("로그인 실패. 다시 시도해보세요.")

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = CustomUser.objects.create_user(email=form.cleaned_data['email'],
            username=form.cleaned_data['username'],
            nickname=form.cleaned_data['nickname'],
            phone_number=form.cleaned_data['phone_number'],
            password=form.cleaned_data['password'])
            login(request, new_user)
            return redirect('home')
    else:
        form = UserForm()
        return render(request, 'myapp/signup.html', {'form': form})

def comment(request, post_id):
    if not request.user.is_active:
        return HttpResponse("Can't write a comment without Sign In")
    
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.c_writer = request.user
            comment.post_id = post
            comment.text = form.cleaned_data['text']
            comment.save()
            return redirect('home')

def hashtag(request, hashtag_name):
    hashtag = get_object_or_404(Hashtag, name=hashtag_name)
    form = CommentForm()
    return render(request, 'myapp/hashtag.html', {'hashtag': hashtag ,'comment_form':form})

def like(request, pk):
    if not request.user.is_active:
        return HttpResponse('First SignIn please')

    posts = get_object_or_404(Post, pk=pk)
    user = request.user

    if posts.likes.filter(id=user.id).exists():
        posts.likes.remove(user)
    else:
        posts.likes.add(user)

    return redirect('home')

def mypage(request, pk):
    user = CustomUser.objects.get(id=pk)
    if user.is_authenticated:
        posts = Post.objects.filter(writer=pk)
        comment_form = CommentForm()
        return render(request, 'myapp/mypage.html', {'posts':posts, 'comment_form':comment_form})