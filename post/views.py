from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Like
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, CommentForm
from django.contrib.auth import login


def home(request):
    return render(request, 'home.html')

def landing_page(request):
    return render(request, 'landing.html')

def about_page(request):
    return render(request, 'about.html')

def tos_page(request):
    return render(request, 'tos.html')

def privacy_page(request):
    return render(request, 'privacy.html')

def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)  # ✅ include FILES for image upload
        if form.is_valid():
            user = form.save()  # form.save() will also handle profile_picture
            login(request, user)  # ✅ log the user in after registration
            return redirect("login")  # redirect to your posts page (or dashboard)
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form, "signup": form})


@login_required
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    temp_var = {"allPosts": posts}
    return render (request, "posts_list.html", {"allPosts": posts})

@login_required
def single_post(request, post_id):
    print("hello")
    post = Post.objects.get(id=post_id)
    print(post)
    return render (request, "singlePost.html", {"post": post, "id": post_id})

@login_required
def new_post(request):
    form = None
    if (request.method == "POST"):
        form = PostForm(request.POST, request.FILES)
        print (form)
        if  (form.is_valid()):
            post = form.save(commit=False)
            post.owner = request.user
            post.save()
            return redirect('posts_list')        
    else:
        form = PostForm() 
    print(form['title'].value())
    print(form.errors)
    return render(request, "new_post.html", {"form": form})

@login_required
def edit_post(request, post_id):

    post = Post.objects.get(id = post_id)
    if (request.method == "POST"):
        form = PostForm(request.POST, request.FILES, instance=post)
        if  (form.is_valid()):
            form.save()
            return redirect('posts_list')
        
    else:
        form = PostForm(instance=post) #create an empty form
    return render(request, "edit_post.html", {"post":post})

@login_required
def delete_post(request, post_id):

    post = Post.objects.get(id = post_id)
    if (request.method == "POST"):
        post.delete()

        return redirect('posts_list')

@login_required   
def view_post(request, post_id):

    post = Post.objects.get(id = post_id)
    print(post)
    if (request.method == "POST"):
        form = PostForm(request.POST, instance=post)
        print (form)
        if  (form.is_valid()):
            form.save()
            return redirect('posts_list')
        
    else:
        form = PostForm(instance=post) #create an empty form
    return render(request, "view_post.html", {"post":post})

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()  # Unlike if already liked

    return redirect("posts_list")

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
    return redirect("posts_list")

    