from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .models import Allposts, Like, Allcomment, Follow_Unfollow, Profile

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        user = Follow_Unfollow.objects.get(user=request.user)
        followed_user = [i for i in user.followed.all()]
        followed_user.append(request.user)
        comments = Allcomment.objects.all().order_by("-pk")[:2]
        post = Allposts.objects.filter(user__in=followed_user).order_by("-pk")
        # post = Allposts.objects.all().order_by("-pk")
        return render(request, "userac/posts.html",{
            "comments" : comments,
            "posts" : post,
        })
        
    messages.error(request, "Please login")
    return redirect("/")


def user_logout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect("/")

def createPost(request):
    if request.method == "POST":
        user = request.user
        caption = request.POST.get("createposttext"," ")
        try:
            image = request.FILES["createpostimg"]
        except:
            image = None
        post_obj = Allposts(user=user, caption=caption, image=image)
        post_obj.save()
        print("POST CREATED")
    return redirect("/accounts/")

def user_profile(request, username):
    user = User.objects.filter(username=username)
    mainfollowed = Follow_Unfollow.objects.get(user=request.user)
    # print(user[0], mainfollowed.get_followed().all())
    if user[0] in mainfollowed.get_followed().all():
        profilefollowed = True
    else:
        profilefollowed = False
    if user:
        profile = Profile.objects.get(user__in=user)
        posts = Allposts.objects.filter(user__in=user).order_by("-pk")
        followed = Follow_Unfollow.objects.filter(user__in=user)
        totalfollowed = followed[0].followed.all()
        totalfollower = followed[0].follower.all()
        # print(user, totalfollowed)
        imageList = [
            posts[i:i+3] for i in range(0, len(posts), 3)
        ]
        return render(request, "userac/userpage.html",{
                "posts" : imageList,
                "totalpost": len(posts),
                "profile" : profile,
                "profilefollowed" : profilefollowed,
                "followed" : len(totalfollowed),
                "follower" : len(totalfollower),
            })
    else:
        return redirect("/accounts/")

def like_dislike_post(request, postid):
    post = Allposts.objects.get(pk=postid)
    user = request.user
    liked_user = Like.objects.filter(post=post, user=user)
    if liked_user:
        Like.dislike(post, user)
    else:
        Like.like(post, user)
    return redirect("/accounts/")

def add_comment(request, postid):
    post = Allposts.objects.get(pk=postid)
    user = request.user
    comment = request.POST.get("commenttext")
    cmt_obj = Allcomment(user=user, post=post, comment=comment)
    cmt_obj.save()
    return redirect("/accounts/")

def delete_post(request, postid):
    post = Allposts.objects.filter(pk=postid)
    post.delete()
    return redirect("/accounts/")


def follow(request, username):
    user = request.user
    to_follow = User.objects.get(username=username)
    follow_user = Follow_Unfollow.objects.filter(user=user, followed=to_follow)
    if follow_user:
        Follow_Unfollow.unfollow(user, to_follow)
        Follow_Unfollow.remove_follower(to_follow, user)
    else:
        Follow_Unfollow.follow(user, to_follow)
        Follow_Unfollow.add_follower(to_follow, user)
    
    return redirect("/")


def show_following(request, username):
    user = User.objects.filter(username=username)
    mainfollowed = Follow_Unfollow.objects.get(user=request.user)
    if user[0] in mainfollowed.get_followed().all():
        profilefollowed = True
    else:
        profilefollowed = False
    if user:
        profile = Profile.objects.get(user__in=user)
        allprofiles = Profile.objects.all()
        posts = Allposts.objects.filter(user__in=user).order_by("-pk")
        followed = Follow_Unfollow.objects.filter(user__in=user)
        totalfollowed = followed[0].followed.all()
        totalfollower = followed[0].follower.all()
        return render(request, "userac/following.html",{
                "totalpost": len(posts),
                "profile" : profile,
                "allprofiles" : allprofiles,
                "profilefollowed" : profilefollowed,
                "followed" : len(totalfollowed),
                "follower" : len(totalfollower),
                "followings" : totalfollowed,
            })
    else:
        return redirect("/accounts/")

def show_follower(request, username):
    user = User.objects.filter(username=username)
    mainfollowed = Follow_Unfollow.objects.get(user=request.user)
    if user[0] in mainfollowed.get_followed().all():
        profilefollowed = True
    else:
        profilefollowed = False
    if user:
        profile = Profile.objects.get(user__in=user)
        allprofiles = Profile.objects.all()
        posts = Allposts.objects.filter(user__in=user).order_by("-pk")
        followed = Follow_Unfollow.objects.filter(user__in=user)
        totalfollowed = followed[0].followed.all()
        totalfollower = followed[0].follower.all()

        return render(request, "userac/follower.html",{
                "totalpost": len(posts),
                "profile" : profile,
                "allprofiles" : allprofiles,
                "profilefollowed" : profilefollowed,
                "followed" : len(totalfollowed),
                "follower" : len(totalfollower),
                "followings" : totalfollowed,
                "followers" : totalfollower,
            })
    else:
        return redirect("/accounts/")

def find_user(request):
    if request.method == "POST":
        username = request.POST.get("username","")
        queryset = User.objects.filter(username__icontains=username)
        profile = Profile.objects.all()
        followed = Follow_Unfollow.objects.get(user=request.user)
        print(username)
        print(followed.followed.all())
        return render(request, "userac/search.html",{
            "queryset" : queryset,
            "profile" : profile,
            "followed" : followed.followed.all()
        })

