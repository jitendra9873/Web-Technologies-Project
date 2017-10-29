from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Student,Follow,Course,Subject,Student_attendance

def base(request):
	return render(request,'frontend.html')

def indexRedirect(request):
    if request.user.is_authenticated():
        return dashboardRedirect(request)
    else:
        return render(request, 'frontend.html')

@login_required
def dashboardRedirect(request):
    return redirect('/user/' + request.user.username + "/dashboard")

def dashboardView(request, username):
    data = {
        "user": getUserData(username, request.user.username),
    }
    return render(request, 'dashboard.html', data)

def signin(request):
    username = request.POST['username']
    password = request.POST['password']
    auth_user = authenticate(request, username=username, password=password)
    if auth_user is not None:
        login(request, auth_user)
        return dashboardRedirect(request)
    else:
        return indexRedirect(request)


def signup(request):
    username = request.POST['username']
    password = request.POST['password']
    fname = request.POST['first_name']
    email = request.POST['email']
    User.objects.create_user(username=username, email=email, password=password, first_name=fname).save()
    auth_user = authenticate(request, username=username, password=password)
    if auth_user is not None:
        Student(username=username, name=fname, email=email).save()
        login(request, auth_user)
        return dashboardRedirect(request)
    else:
        return indexRedirect(request)


def signout(request):
    logout(request)
    return redirect("/")

def profile(request, username):
    user = Student.objects.filter(username__iexact=username).first()
    data={
        "user":user,
    }
    return render(request, 'profile.html', data)

def Mycourse(request, username):
    user = Student.objects.filter(username__iexact=username).first()
    c=user.course
    print(c)
    obj = Course.objects.filter(coursename=c).first()
    print(obj)
    data={
        "user":user,
        "cour":obj,
    }
    return render(request, 'course.html', data)


def indexView(request):
	return render(request, 'frontend.html')


def followersView(request, username):
    data = {
        "type": "Followers",
        "user": getUserData(username, request.user.username),
        "people": getFollowerData(username),
    }
    return render(request, 'people.html', data)


def followingsView(request, username):
    data = {
        "type": "Following",
        "user": getUserData(username, request.user.username),
        "people": getFollowingData(username),
    }
    return render(request, 'people.html', data)


def attendance(request, username):
    user = Student.objects.filter(username__iexact=username).first()
    attend=Student_attendance.objects.filter(student=user).first()
    data = {
        "user":user,
        "attend": attend,
    }
    return render(request, 'attendance.html', data)


def getUserData(username, logined_username):
    user = Student.objects.filter(username__iexact=username).first()

    if logined_username:
        curr_user = Student.objects.filter(username__iexact=logined_username).first()
        #user_img = curr_user.avatar
        follow_button = (not Follow.objects.filter(follower=curr_user, followed=user))
    else:
        user_img = None
        follow_button = None
    user_img = None
    if user is None:
        raise Http404("User does not exist")

    following_count = Follow.objects.filter(follower=user).count()

    return {
        "name": user.name,
        "course":user.course,
        "username": user.username,
        "email": user.email,
        #"img": user.avatar,
        "user_img": user_img,
        "following": following_count,
        "follow_button": follow_button,
    }

def getFollowerData(username):
    user = Student.objects.filter(username__iexact=username).first()

    if user is None:
        raise Http404("User does not exist")

    followers = Follow.objects.filter(followed=user)

    f_list = list()
    for f in followers:
        f_list.append({
            "name": f.follower.name,
            "username": f.follower.username,
            "email": f.follower.email,
            "img": f.follower.avatar,
        })

    return f_list


def getFollowingData(username):
    user = Student.objects.filter(username__iexact=username).first()

    if user is None:
        raise Http404("User does not exist")

    following = Follow.objects.filter(follower=user)

    f_list = list()
    for f in following:
        f_list.append({
            "name": f.followed.name,
            "username": f.followed.username,
            "email": f.followed.email,
            "img": f.followed.avatar,
        })

    return f_list
