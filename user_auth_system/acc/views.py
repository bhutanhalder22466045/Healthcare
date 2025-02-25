from django.contrib.auth import login, logout, authenticate
from .forms import SignupForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog
from .forms import BlogForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Blog



@login_required
def create_blog(request):
    if request.user.user_type != 'doctor':
        return redirect('home')

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user  # Set current user as author
            blog.save()
            return redirect('my_blogs')
    else:
        form = BlogForm()

    return render(request, 'create_blog.html', {'form': form})



@login_required
def my_blogs(request):
    if request.user.user_type != 'doctor':
        return redirect('home')
    blogs = Blog.objects.filter(author=request.user)
    return render(request, 'my_blogs.html', {'blogs': blogs})


# List of Blogs (Patients View - Only Published Blogs)
def blog_list(request):
    categorized_blogs = {}
    categories = ['Mental Health', 'Heart Disease', 'Covid19', 'Immunization']

    for category in categories:
        categorized_blogs[category] = Blog.objects.filter(category=category, is_draft=False)

    return render(request, 'patientblog.html', {'categorized_blogs': categorized_blogs})


@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    # Ensure only the author (doctor) can delete their own post
    if request.user == blog.author:
        blog.delete()
        return redirect('my_blogs')  # Redirect to the user's blog list after deletion

    return redirect('home')  # Redirect to home if unauthorized

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')


def dashboard_view(request):
    if request.user.is_authenticated:
        return render(request, f"{request.user.user_type}_dashboard.html", {'user': request.user})
    return redirect('login')


def logout_view(request):
    logout(request)
    return redirect('login')
