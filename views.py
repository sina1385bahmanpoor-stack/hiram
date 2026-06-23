from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView, View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import User
from .forms import SignUpForm, LoginForm


class SignUpView(FormView):
    template_name = 'users/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ثبت‌نام'
        return context


class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ورود'
        return context


class LogoutView(LoginRequiredMixin, TemplateView):
    template_name = 'users/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


class HomeView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        user = request.user
        
        # اگر دانش‌اموز است
        if user.user_type == 'student':
            return redirect('student_home')
        
        # اگر ادمین است
        elif user.user_type == 'admin':
            return redirect('admin_home')
        
        # اگر مشاور است
        elif user.user_type == 'advisor':
            return redirect('advisor_home')
        
        # اگر سوپر یوزر
        elif user.is_superuser:
            return redirect('admin_home')


class StudentHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'users/student_home.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        
        # سریال رابطه‌ی این دانش‌اموز
        try:
            relationship = user.as_student
            context['advisor'] = relationship.advisor
            context['admin'] = relationship.admin
        except:
            context['advisor'] = None
            context['admin'] = None
        
        return context
    
    def get(self, request, *args, **kwargs):
        # تنها دانش‌اموزان می‌تونند وارد شوند
        if request.user.user_type != 'student':
            return redirect('home')
        return super().get(request, *args, **kwargs)


class AdminHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'users/admin_home.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        
        # تمام دانش‌اموزانی که تحت نظارت این ادمین هستند
        students = user.students_under_admin.all()
        context['students'] = students
        
        return context
    
    def get(self, request, *args, **kwargs):
        # تنها ادمین‌ها و سوپر یوزرها می‌تونند وارد شوند
        if request.user.user_type != 'admin' and not request.user.is_superuser:
            return redirect('home')
        return super().get(request, *args, **kwargs)


class AdvisorHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'users/advisor_home.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        
        # تمام دانش‌اموزانی که تحت نظارت این مشاور هستند
        students = user.students_under_advisor.all()
        context['students'] = students
        
        return context
    
    def get(self, request, *args, **kwargs):
        # تنها مشاورها می‌تونند وارد شوند
        if request.user.user_type != 'advisor':
            return redirect('home')
        return super().get(request, *args, **kwargs)
