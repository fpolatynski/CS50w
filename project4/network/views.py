import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post


def index(request):
    return render(request, "network/index.html", {"current_user": request.user.id})


def following(request):
    return render(request, "network/following.html", {"current_user": request.user.id})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
def add_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data["text"])
        # Adding POSTs to database
        post = Post(text=data["text"], owner=request.user)
        post.save()
        return JsonResponse({"message": "Email sent successfully."}, status=201)


def posts(request):
    page = int(request.GET.get('page'))
    user = request.GET.get('owner')
    if user is None:
        posts_to_display = Post.objects.all().order_by("-timestamp")
    else:
        if user == "f":
            follows = request.user.follows.all()
            posts_to_display = Post.objects.filter(owner__in=follows).order_by("-timestamp")
        else:
            posts_to_display = Post.objects.filter(owner_id=int(user)).order_by("-timestamp")
    paginator = Paginator(posts_to_display, 10)

    return JsonResponse({
        "posts": [x.serializes() for x in paginator.get_page(page).object_list],
        "current_user": request.user.serializes()
    })


def profile_page(request, user_id):
    user = User.objects.get(pk=user_id)
    cur_user = request.user
    if request.method == "POST":
        if_follow = request.POST.get("follow")
        if if_follow == "follow":
            cur_user.follows.add(user)
        elif if_follow == "unfollow":
            cur_user.follows.remove(user)

    follow = user.followers.filter(pk=request.user.id)
    return render(request, "network/user_page.html", user.serializes() | {
        "follow": len(follow),
        "current_user": request.user.id
    })


@csrf_exempt
def like(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = int(data["post_id"])
        is_like = data["like"]
        if post_id:
            if is_like:
                request.user.liked_posts.add(Post.objects.get(pk=post_id))
            else:
                request.user.liked_posts.remove(Post.objects.get(pk=post_id))
            return JsonResponse({'answear': "Liked sucesfully"}, status=201)
        else:
            return JsonResponse({'answear': "Something went wrong"}, status=201)
