from django.urls import path
from django.shortcuts import render
from .views import signup_view, login_view, dashboard_view, logout_view


def home_view(request):
    return render(request, 'home.html')


urlpatterns = [
    path('', home_view, name='home'),  # Home page
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
]