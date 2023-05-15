from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from app.forms import *
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
 
def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        D={'username':username}
        return render(request,'home.html',D)
    return render(request,'home.html')







def register(request):
    ufo=Userforms()
    pfo=Profileforms()
    d={'ufo':ufo,'pfo':pfo}
    if request.method=='POST' and request.FILES:
        UOD=Userforms(request.POST)
        POD=Profileforms(request.POST,request.FILES)
        if UOD.is_valid() and POD.is_valid():
            NUOD=UOD.save(commit=False)
            NUOD.set_password(UOD.cleaned_data['password'])
            NUOD.save()

            NPOD=POD.save(commit=False)
            NPOD.username=NUOD
            NPOD.save()

            #send_mail('subject','message/content of mail','from mail id', recipient_list',fail_silent=True)
            send_mail('Rigistraion is done successfully..!',
                      "iam a developer at jspyders we are hiring if you want to intrested join our company",
                      'npersonal47@gmail.com',
                      [NUOD.email],
                      fail_silently=True )
            return HttpResponse('registraion is done...!')
        else:
            return HttpResponse('invalid data..!')
    
    return render(request,'register.html',d)



def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        auo=authenticate(username=username,password=password)
        if auo and auo.is_active:
            login(request,auo)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('invalid username and password')  
    return render(request,'user_login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required
def display_profile(request):
    username=request.session.get('username')
    uo=User.objects.get(username=username)
    po=Profile.objects.get(username=uo)
    d={'uo':uo,'po':po}
    return render(request,'display_profile.html',d)

@login_required
def change_password(request):
   if request.method=='POST':
        pw=request.POST['pw']
        username=request.session.get('username')
        uo=User.objects.get(username=username)
        uo.set_password(pw)
        uo.save()
        return HttpResponse('Password is changed successfully')
   return render(request,'change_password.html')


def forgot_pw(request):
   if request.method=='POST':
        uo=request.POST['uo']
        po=request.POST['po']
        lUO=User.objects.filter(username=uo)
        if lUO:
            UO=lUO[0]
            UO.set_password(po)
            UO.save()
            
        else:
            return HttpResponse('username is not registered...!')
        return HttpResponse('your new password is updated is done...!')
       
   return render(request,'forgot_pw.html')

