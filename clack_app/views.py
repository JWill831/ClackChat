from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.conf import settings

import bcrypt
# Create your views here.
def home(request):
    if request.method=="GET":
        if 'userid' not in request.session:
            context = {
            'messages' : Message.objects.all().order_by('-created_at'),
            # 'message': Message.objects.get(id=request.FILES['image_name'])
            # 'image': image,
            # 'new_image':last_image
            }
            return render(request, "home.html", context)
        else:
            # last_image=Message.image.last()
            # image=Message.image.all()
            context = {
            'user': User.objects.get(id=request.session["userid"],),
            'messages' : Message.objects.all().order_by('-created_at'),
            # 'message': Message.objects.get(id=request.FILES['image_name'])
            # 'image': image,
            # 'new_image':last_image
            }
            # message1=Message.objects.last().image
            # print(message1)
            return render(request, "home.html", context)
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        fs = FileSystemStorage()
        filename = fs.save(request.FILES['image_name'].name, request.FILES['image_name'])
        uploaded_file_url = fs.url(filename)
        return redirect("/home")

def register(request):
    if request.method=="GET":
        return render(request, "login_registration.html")
    if request.method=="POST":
        errors = User.objects.r_validator(request.POST)
    # when registration fails
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v, extra_tags = k)
            # put the return one indent out.
        return redirect("/register")
    else:
        #success
        hashbrown = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        User.objects.create(
            user_name= request.POST['user_name'],
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashbrown
        )
        request.session['userid'] = User.objects.last().id
        return redirect("/")

def login(request):
    errors = User.objects.l_validator(request.POST)
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v, extra_tags = k)
            # put the return one indent out.
        return redirect("/register")
    else:
        u = User.objects.get(email=request.POST['login_email'])
        request.session['userid'] = u.id
        return redirect("/")

def login_admin(request):
    errors = User.objects.a_validator(request.POST)
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v, extra_tags = k)
            # put the return one indent out.
        return redirect("/admin")
    else:
        u = User.objects.get(email=request.POST['login_email'])
        request.session['userid'] = u.id
        return redirect("/")

def logout(request):
    request.session.flush()
    return redirect("/")

def message(request):
    if request.method == "GET":
        context ={
            'fs' : FileSystemStorage(),
            'filename' : fs.save(request.FILES['image_name'].name, request.FILES['image_name']),
            'uploaded_file_url' :rl(filename),
            'messages' : Message.objects.all().order_by('created_at'),
            'user' : User.objects.get(id=request.session['userid']),
        }
        
        return render(request, "home.html", context)
    if request.method == "POST":
        if request.POST['message'] != '':
            user = User.objects.get(id=request.session['userid'])
            # Message.objects.create(user=user,message=request.POST['message'])
        
        if 'image_name' in request.FILES:
            fs = FileSystemStorage()
            filename = fs.save(f"{request.session['userid']}/" + request.FILES['image_name'].name, request.FILES['image_name'])
            uploaded_file_url = fs.url(filename)
            Message.objects.create(user=User.objects.get(id=request.session['userid']), image=uploaded_file_url,message=request.POST['message'])
        else:
            uploaded_file_url = None
            Message.objects.create(user=User.objects.get(id=request.session['userid']), image=uploaded_file_url,message=request.POST['message'])
        return redirect("/")

def admin(request):
    if request.method=="GET":
        return render(request, "admin.html")
    if request.method=="POST":
        errors = User.objects.a_validator(request.POST)
        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v, extra_tags = k)
            return redirect("/")
    
def delete(request, id):
    this_msg=Message.objects.get(id=id)
    this_msg.delete()
    return redirect("/")

def videos(request):
    return render(request, 'videos.html')

def articles(request):
    return render(request, 'articles.html')

def vendors(request):
    return render(request, 'vendors.html')

def qmk(request):
    return render(request, 'qmk.html')

def games(request):
    return render(request, 'games.html')