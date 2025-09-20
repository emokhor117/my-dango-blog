from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.contrib.auth import login

def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


@login_required
def post_list(request):
    posts = Post.objects.filter(owner=request.user)
    temp_var = {"allPosts": posts}
    return render (request, "posts_list.html", temp_var)

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

    