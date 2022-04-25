from django.shortcuts import render
from user_app.forms import UserForm,UserInfoForm
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
def index(request):
    return render(request,'user_app/index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def register(request):
    registered=False
    if request.method=="POST":
        user_form=UserForm(data=request.POST)
        profile_form=UserInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()
            profile=profile_form.save(commit=False)
            profile.user=user
            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']
            profile.save()
            registered=True
        else:
             print(user_form.errors,profile_form.errors)


    else:
        user_form=UserForm()
        profile_form=UserInfoForm()
    return render(request,'user_app/registration.html',{'UserInfo':user_form,'profile_info':profile_form,'registration':registered})



def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account not Active")
        else:
            print("Someone with Username:{} and Password:{} tried to login".format(username,password))
            return HttpResponse("Invalid Login Details ")
    else:
        return render(request,'user_app/login.html',{})
