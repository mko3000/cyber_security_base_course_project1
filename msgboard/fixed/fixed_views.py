from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.urls import reverse
from .fixed_models import Message, BadMessage, BadUser

def home(request):
    account_link = '/account/'
    return render(request, 'home.html', {'account_link': account_link})

def login_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        action = request.POST.get('action')
        
        if action == 'login':
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                if not User.objects.filter(username=username).exists():
                    error = "Wrong credentials. Try other credentials or register a new user"
                    login(request, user)
                    return render(request, 'login.html', {'error': error})
                else:
                    # User exists but password is incorrect
                    error = "Wrong credentials. Try other credentials or register a new user"
                    return render(request, 'login.html', {'error': error})
        if action == 'register':
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password)
                login(request, user)
                return redirect('home')     
                     
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/login')
def messages_view(request):
    messages = Message.objects.all().order_by('-created_at')
    return render(request, 'messages.html', {'messages': messages})

@login_required(login_url='/login')
def add_view(request):
    Message.objects.create(poster =request.user, content=request.POST.get('content'))
    return redirect('messages')

@login_required(login_url='/login')
def account_view(request):
    user = request.user
    messages = Message.objects.filter(user = user)       
    return render(request, 'account_page.html', {'messages': messages})

@login_required(login_url='/login')
def delete(request):
    user = request.user
    msg_id = request.POST.get('msg_id')
    message = Message.objects.get(id=msg_id)
    #additional check that the user actually posted the message
    if message.poster == user:
        Message.objects.filter(id=msg_id).delete()
    return redirect('account')