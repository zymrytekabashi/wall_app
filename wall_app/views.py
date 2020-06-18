from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import User, UserManager, Message, Comment
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

def create_user(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
        user=User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'],bday=request.POST['bday'], email=request.POST['email'], password= password)
        request.session['uid']= user.id
        return redirect('/success')
    
    
    
        
def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if len(user) > 0:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['uid'] = logged_user.id
            return redirect('/success')
        else:
            message.error(request, 'Email and password did not match')
            
    else:
        messages.error(request, 'Email is not registered')
    return redirect('/')
        


def success(request):
    context = {
        'user':User.objects.get(id=request.session['uid']),
        'all_messages': Message.objects.all(),
        'comments': Comment.objects.all()
    }
    
    return render(request, 'success.html',context)

def create_message(request):
    Message.objects.create(message = request.POST['message'], poster=User.objects.get(id=request.session['uid']))
    return redirect('/success')

def post_comment(request, mess_id):
    Comment.objects.create(comment=request.POST['comment'], poster=User.objects.get(id=request.session['uid']), message=Message.objects.get(id=mess_id))
    return redirect('/success')

def log_out(request):
    request.session.clear()
    return redirect('/')
