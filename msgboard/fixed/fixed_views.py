from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.utils.module_loading import import_string
from django.core.exceptions import (
    ImproperlyConfigured,
    ValidationError,
)
import logging
from django.contrib.auth.signals import user_login_failed
from .fixed_models import Message

log = logging.getLogger(__name__)

def get_client_ip(request):
    """Extract client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def validate_password(password, user=None):    
    errors = []
    for validator in settings.AUTH_PASSWORD_VALIDATORS:
        try:
            klass = import_string(validator["NAME"])
        except ImportError:
            msg = (
                "The module in NAME could not be imported: %s. Check your "
                "AUTH_PASSWORD_VALIDATORS setting."
            )
            raise ImproperlyConfigured(msg % validator["NAME"])
        curValidator = klass(**validator.get("OPTIONS", {}))
        try:
            curValidator.validate(password, user)
        except ValidationError as error:
            errors.append(error)
    if errors:
        raise ValidationError(errors)

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
                    log.warning(f"Login failed for non-existent user: {username} from IP: {get_client_ip(request)}")
                    user_login_failed.send(sender=get_client_ip(request), credentials={"username": username}, request=request)
                    return render(request, 'login.html', {'error': error})
                else:
                    # User exists but password is incorrect
                    error = "Wrong credentials. Try other credentials or register a new user"
                    log.warning(f"Login failed for user: {username} from IP: {get_client_ip(request)}")
                    user_login_failed.send(sender=get_client_ip(request), credentials={"username": username}, request=request)
                    return render(request, 'login.html', {'error': error})
        if action == 'register':
            if not User.objects.filter(username=username).exists():
                validate_password(password, username)
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