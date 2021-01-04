from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from userac.models import Profile, Follow_Unfollow

# Create your views here.
def index(request):
    if request.user.is_authenticated:
       return redirect("/accounts")
        
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        # print("login:",username, password)

        user_obj = authenticate(username=username, password=password)
        if user_obj is not None:
            login(request, user_obj)
            return redirect("/accounts")
        else:
            messages.error(request, "invalid cradencial")
            return redirect("/")

    return render(request, "accounts/index.html")

def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        fname = request.POST.get("fullname")
        password = request.POST.get("password")
        cnfpassword = request.POST.get("cnfpassword")
        print("register", username, fname, password, cnfpassword)
        if password == cnfpassword:
            user_obj = User.objects.create_user(
                username=username,
                first_name=fname,
                password=password,
                )
            user_obj.save()
            profile = Profile(user=user_obj)
            profile.save()
            follow = Follow_Unfollow(user=user_obj)
            follow.save()
            messages.success(request, " Account created now login")
        else:
            messages.error(request, "Password not matched")
        
        return render(request, "accounts/index.html")

    return render(request, "accounts/register.html")