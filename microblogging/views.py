import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Post, Relation
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.paginator import Paginator


def index(request):
    if request.method == 'POST':
        newPost = Post(username=request.user, postcontent=request.POST['newPost'])
        newPost.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        allPostsInReverse = Post.objects.order_by('-pk').all()
        paginator = Paginator(allPostsInReverse, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "microblogging/index.html", {
            # "posts" : Post.objects.order_by('-pk').all()
            "page_obj": page_obj
        })


def following(request):
    if (request.user.is_authenticated):
        allPosts = []
        follows = Relation.objects.filter(follower=request.user)
        posts = Post.objects.order_by('-pk').all()

        for post in posts:
            for followed in follows:
                if post.username == followed.followed:
                    allPosts.append(post)

        paginator = Paginator(allPosts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "microblogging/following.html", {
            "page_obj": page_obj,
        })
    else:
        return HttpResponse('404: You must Log In to view this page')


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
            return render(request, "microblogging/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "microblogging/login.html")


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
            return render(request, "microblogging/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "microblogging/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "microblogging/register.html")


# def addLike
@csrf_exempt
def likeUnlike(request, postid):
    if request.method == "POST":
        postObject = Post.objects.get(pk=postid)
        if (request.user in postObject.likedBy.all()):
            postObject.likedBy.remove(request.user)
            return JsonResponse({
                "result": f"Removed user {request.user.username} from likedBy"
            })
        else:
            postObject.likedBy.add(request.user)
            return JsonResponse({
                "result": f"Added user {request.user.username} to likedBy"
            })


@csrf_exempt
def removepost(request, postid):
    if request.method == "POST":
        postObject = Post.objects.get(pk=postid)
        if (postObject.username == request.user):
            postObject.delete()
            # print('Removed user from like');
            return JsonResponse({
                "result": f"Deleted Post:{postid} from Database"
            })
        else:
            return JsonResponse({
                "result": f"You dont have rights to delete the Posts"
            })


@csrf_exempt
def editPost(request, postid):
    if request.method == "PUT":
        postObject = Post.objects.get(pk=postid)
        print(postObject.postcontent)
        data = json.loads(request.body)
        print(postObject.username)
        if (postObject.username == request.user):
            postObject.postcontent = data["postcontent"]
            postObject.save()
            return JsonResponse({
                "result": f"Edited Post:{postid} from Database"
            })
        else:
            return JsonResponse({
                "result": f"You dont have rights to Edit the Posts"
            })


@csrf_exempt
def profilePage(request, userName):
    selectedUser = User.objects.get(username=userName)
    try:
        followRelation = Relation.objects.get(follower=request.user, followed=selectedUser)
        doIFollow = "true"
    except:
        doIFollow = "false"

    posts = Post.objects.order_by('-pk').filter(username=selectedUser)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "microblogging/profile.html", {
        "page_obj": page_obj,
        "selectedUser": selectedUser.username,
        "followers": selectedUser.followers.all().count(),
        "follows": selectedUser.follows.all().count(),
        "doIFollow": doIFollow,
    })


@csrf_exempt
def toggleFollow(request, userName):
    if request.method == "POST":
        selectedUser = User.objects.get(username=userName)
        try:
            followRelation = Relation.objects.get(follower=request.user, followed=selectedUser)
            followRelation.delete()
            # followRelation.save()
            return JsonResponse({
                "result": "You have UnFollowed the User"
            })

        except:
            followRelation = Relation.objects.create(follower=request.user, followed=selectedUser)
            followRelation.save()
            return JsonResponse({
                "result": "You have now followed the user"
            })
