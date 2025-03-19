from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_register, name='login'),
    path('messages/', views.messages_view, name='messages'),
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.add_view, name='add'),
    path('account/', views.account_view, name='account'),
    path('delete/', views.delete, name='delete')
]