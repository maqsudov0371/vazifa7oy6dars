import datetime
from typing import Any
from django.http import FileResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from django.views import View
from .models import User, Course, Category, Tag, Header, HeaderImage, News, Comment
from django.contrib.messages import warning, success
from .utils import send_verification_email
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .forms import CourseForm
# Create your views here.

class HomePageView(ListView):
    model = Course
    template_name = 'index.html'
    context_object_name = 'courses'
    paginate_by = 3


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        try:
            header = Header.objects.first()
            context['header'] = header
            header_images = HeaderImage.objects.filter(header=header)
            context['header_images'] = header_images
        except:
            pass
        return context
    
    

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
    
    def post(self, request):
        username = request.POST['username']
        email = request.POST.get('email')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        phone = request.POST.get('phone')
        
        if password != password_confirm:
            warning(request, 'Password confirmation is incorrect')
            return redirect(reverse('main:register'))
        if User.objects.filter(username=username).exists():
            warning(request, 'User already registered')
            return redirect(reverse('main:register'))
        user = User.objects.create_user(username=username, 
                                        email=email,
                                        password=password,
                                        phone=phone, is_active=False)
        send_verification_email(user)
        login(request, user)
        success(request, 'User  registered')
        return redirect(reverse("main:kirish"))


class LoginView(View):
    def get(self, request):
        return render(request, 'registration/login.html', {"success": True})
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username=username).exists():
            warning(request, 'User does not exist')
            return redirect(reverse('main:kirish'))
        user = User.objects.get(username=username)
        if not user.check_password(password):
            warning(request, 'Password is incorrect')
            return redirect(reverse('main:kirish'))
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('main:home'))
        warning(request, 'Error')
        return redirect(reverse('main:kirish'))
        


class CourseDetailView(DetailView):
    model = Course
    template_name = 'course_single.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:    
        data = super().get_context_data(**kwargs)
        data['tags'] = Tag.objects.all()
        return data


import os


class AddCourseView(View):
    model = Course
    fields = "__all__"  #['title','created_at', 'description', 'duration', 'price', 'category', 'language', 'tags', 'image']
    template_name = 'course_add.html'
    success_url = "/"
    
    def get(self, request):
        path = os.getcwd()
        file = open(f"{path}/main/forms.py", 'rb')
        return JsonResponse({'success': True})
        form = CourseForm()
        return render(request, self.template_name, {'form': form, 'button': 'Add'})

    def post(self, request):
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            success(request, 'Course added successfully')
            return redirect(self.success_url)
        else:
            warning(request, 'Course adding failed')
            return render(request, self.template_name, {'form': form})


class UpdateCourseView(View):
    model = Course
    fields = "__all__"  #['title','created_at', 'description', 'duration', 'price', 'category', 'language', 'tags', 'image']
    template_name = 'course_add.html'
    success_url = "/"

    def get(self, request, pk):
        lang = request.COOKIES.get('language')
        button = 'Yangilash'
        if lang == 'en':
            button = 'Update'
        if lang == 'ru':
            button = 'Обновить'

        course = Course.objects.get(pk=pk)
        form = CourseForm(instance=course)
        response = render(request, self.template_name, {'form': form, 'button': button})
        expiry_time = datetime.datetime.now() + datetime.timedelta(hours=2)
        response.set_cookie('language', "uz", 7200)
        return response


    def post(self, request, pk):
        course = Course.objects.get(pk=pk)
        title = request.POST.get('title')
        course.title = title
        course.save()

from .models import News, Comment

class NewsListView(ListView):
    model = News
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10

class NewsDetailView(DetailView):
    model = News
    template_name = 'news_detail.html'
    context_object_name = 'news'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        data = super().get_context_data(**kwargs)
        data['comments'] = Comment.objects.filter(news=self.object)
        return data
