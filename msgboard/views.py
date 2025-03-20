from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.urls import reverse
from .models import BadMessage, BadUser

def getUser(request):
    user_id = request.COOKIES.get("user_id")
    if not user_id:
        return    
    return BadUser.objects.get(id = user_id.split("_")[0])

def home(request):
    user = getUser(request)
    account_link = '/account/'
    if user:
        account_link = f'/account?user={user.username}'
    return render(request, 'home.html', {'account_link': account_link})
    
def login_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        action = request.POST.get('action')
        
        if action == 'login':
            if not BadUser.objects.filter(username=username).exists():
                #no user found
                error = "Username doesn't exist. Register user or try another username."
                return render(request, 'login.html', {'error': error})
            else:
                #user found
                user = BadUser.objects.get(username=username)
                if password != user.password:
                    error = "Invalid password. Please try again."
                    return render(request, 'login.html', {'error': error})
                else:
                    response = redirect('home')
                    user_id = f'{user.id}_{user.username}'
                    response.set_cookie('user_id', user_id, max_age=99999999)
                    return response
                
        if action == 'register':
            if not BadUser.objects.filter(username=username).exists():
                user = BadUser.objects.create(username=username, password=password)
                response = redirect('home')
                user_id = f'{user.id}_{user.username}'
                response.set_cookie('user_id', user_id, max_age=99999999)
                return response
            else:
                error = "User already exists."
                return render(request, 'login.html', {'error': error})
                     
    return render(request, 'login.html')

@csrf_exempt 
def logout_view(request):
    response = redirect('home')
    response.delete_cookie("user_id")
    return response

@csrf_exempt
def messages_view(request):
    messages = BadMessage.objects.all().order_by('-created_at')
    return render(request, 'messages.html', {'messages': messages})

@csrf_exempt
def add_view(request):
    user = getUser(request)
    BadMessage.objects.create(poster=user, content=request.POST.get('content'))
    return redirect('messages')

@csrf_exempt
def account_view(request):
    username = request.GET.get('user')
    user = BadUser.objects.filter(username=username).first()
    messages = BadMessage.objects.filter(poster = user)       
    return render(request, 'account_page.html', {'messages': messages, 'username': username})

@csrf_exempt
def delete(request):
    user = getUser(request)
    msg_id = request.POST.get('msg_id')
    BadMessage.objects.filter(id=msg_id).delete()
    account_url = reverse('account') 
    return redirect(f'{account_url}?user={user}')