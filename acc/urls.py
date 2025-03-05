from django.urls import path
from django.shortcuts import render
from .views import signup_view, login_view, dashboard_view, logout_view, list_doctors, book_appointment
from .views import create_blog, my_blogs, blog_list
from .views import delete_blog, appointment_success


def home_view(request):
    return render(request, 'home.html')


urlpatterns = [
    path('', home_view, name='home'),
    path('create-blog/', create_blog, name='create_blog'),
    path('my-blogs/', my_blogs, name='my_blogs'),
    path('blogs_list/', blog_list, name='blogs_list'),
    path('delete-blog/<int:blog_id>/', delete_blog, name='delete_blog'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('doctors/', list_doctors, name='list_doctors'),
    path('book-appointment/<int:doctor_id>/', book_appointment, name='book_appointment'),
    path("appointment-success/<int:appointment_id>/", appointment_success, name="appointment_success"),
]
