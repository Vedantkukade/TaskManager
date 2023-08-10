from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from todoapp.forms import RegistrationForm
from django.contrib.auth.models import User
from todoapp.models import TaskModel
import datetime
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
import random


def user_register(request):
    content={}
    if request.method=="POST":
        un=request.POST['uname']
        p=request.POST['upass']
    
        cp=request.POST['ucpass']


        if un=='' or p=='' or cp=='':
            content['errmsg']="Field cannot empty"
        elif p!=cp:
            content['errmsg']="Password doesn't match"
        elif len(p)<8:
            content['errmsg']="Password must be 8 characters in length"
        else:

            try:
                u=User.objects.create(username=un,email=un)
                u.set_password(p)
                u.save()
                content['success']="User registerd successfully!"
            except Exception:
                content['errmsg']="User with same name is already exist"
        return render(request,'accountsapp/register.html',content)
    else:
        return render(request,'accountsapp/register.html')


def user_login(request):
    content={}
    if request.method=="POST":
        un= request.POST['uname']
        p= request.POST['upass']
        u=authenticate(username=un,password=p)
    
        if u is not  None:
            login(request,u)
            return redirect('/dashboard')
        else:
            content['errmsg']="invalid username  or password"
            return render(request,'accountsapp/login.html',content)
    else: 
        return render(request,'accountsapp/login.html')


def user_logout(request):
    logout(request) 
    return redirect('/login')


def delete(request,rid):
    
    t=TaskModel.objects.filter(id=rid)
    t.update(is_deleted=True)
    return redirect('/dashboard')

def edit(request,rid):
    if request.method=="POST":
        uname=request.POST['tname']
        udet=request.POST['tdetails']
        uc=request.POST['cat']
        us=request.POST['status']
        udt=request.POST['duedate']

        t=TaskModel.objects.filter(id=rid)
        t.update(name=uname,detail=udet,category=uc,status=us,end_date=udt)
        return redirect('/dashboard')
    
    else:
        
        t=TaskModel.objects.filter(id=rid)
        content={}
        content['data']=t
        return render(request,'todoapp/edit.html',content)

def catfilter(request,cv):
    q1=Q(uid=request.user.id)
    q2=Q(is_deleted=False)
    q3=Q(category=cv)

    t=TaskModel.objects.filter(q1 & q2 & q3)
    content={}
    content['data']=t
    return render(request,'todoapp/dashboard.html',content)


def statfilter(request,sf):
    q1=Q(uid=request.user.id)
    q2=Q(status=False)
    q3=Q(status=sf)
    t=TaskModel.objects.filter(q1 & q2 & q3)
    content={}
    content['data']=t
    return render(request,'todoapp/dashboard.html',content)

def datefilter(request):
    frm=request.GET['from']
    to=request.GET['to']
    
    q1=Q(uid=request.user.id)
    q2=Q(is_deleted=False)
    q3=Q(end_date__gte=frm)
    q4=Q(end_date__lte=to)
    t=TaskModel.objects.order_by('-end_date').filter(q3 & q4).filter(q1 & q2)
    content={}
    content['data']=t

    return render(request,'todoapp/dashboard.html',content)

def datesort(request,dv):
    q1=Q(uid=request.user.id)
    q2=Q(is_deleted=False)
    if dv=='0':
        col='-end_date'
    else:
        col='end_date'
    
    t=TaskModel.objects.order_by(col).filter(q1 & q2)
    
    content={}
    content['data']=t

    
    return render(request,'todoapp/dashboard.html',content)






def dashboard(request):
    content={}

    if request.method=="POST":
        name=request.POST['tname']
        det=request.POST['tdetails']
        cat=request.POST['cat']
        sta=request.POST['status']
        due=request.POST['duedate']

   

        u=User.objects.filter(id=request.user.id) 
        t=TaskModel.objects.create(name=name,detail=det,category=cat,status=sta,end_date=due,created_on=datetime.datetime.now(),uid=u[0])
        t.save()
        return redirect('/dashboard')

    else:
        q1=Q(uid=request.user.id)
        q2=Q(is_deleted=False)
        t=TaskModel.objects.filter(q1 & q2)

        
        content['data']=t
        sendpendingemail(t)
        return render(request,'todoapp/dashboard.html',content)


def sendpendingemail(t):

    for x in t:
        if x.status==0:
            d=x.end_date.day
            curdt=datetime.datetime.now().day
            diff=d-curdt
            if diff==1:
                rec=x.uid.email
                subject='REMINDER'
                msg=x.name+" Task is due for 1 day"
                sender='vedu.kukade@gmail.com'
                send_mail(
                    subject,
                    msg,
                    sender,
                    [rec],
                    fail_silently=False,
                )

    

