from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Like, Profile
from .forms import PostForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, CommentForm
from django.contrib.auth import login
from django.utils.timezone import now



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
def view_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, "view_profile.html", {"profile": profile})

@login_required
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')

    # attach a flag to each post
    for post in posts:
        post.is_liked = post.likes.filter(user=request.user).exists()

    return render(request, "posts_list.html", {"allPosts": posts})

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
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')

        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        user.save()
        profile.save()
        return redirect('view_profile')

    return render(request, "edit_profile.html", {"profile": profile})


@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()
        is_liked = False
    else:
        is_liked = True

    return JsonResponse({
        "is_liked": is_liked,
        "likes_count": post.likes.count()
    })
 # for now just reload the page

@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get("content", "").strip()

        if content:
            comment = Comment.objects.create(
                post=post,
                user=request.user,
                content=content,
                created_at=now()
            )
            return JsonResponse({
                "username": comment.user.username,
                "profile_pic": comment.user.profile.profile_picture.url if comment.user.profile.profile_picture else "/media/profile_pictures/default.jpg",
                "content": comment.content,
                "created_at": comment.created_at.strftime("%b %d, %Y %H:%M"),
            })
    return JsonResponse({"error": "Invalid request"}, status=400)


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
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    is_liked = post.likes.filter(user=request.user).exists()  # ✅ check here

    return render(request, "view_post.html", {
        "post": post,
        "comments": comments,
        "is_liked": is_liked
    })




    