from django.urls import path
from django.shortcuts import render
from .views import signup_view, login_view, dashboard_view, logout_view
from django.urls import path
from .views import create_blog, my_blogs, blog_list
from .views import delete_blog


def home_view(request):
    return render(request, 'home.html')


urlpatterns = [
    path('create-blog/', create_blog, name='create_blog'),
    path('my-blogs/', my_blogs, name='my_blogs'),
    path('blogs_list/', blog_list, name='blogs_list'),
    path('', home_view, name='home'),
    path('delete-blog/<int:blog_id>/', delete_blog, name='delete_blog'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
]