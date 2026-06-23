from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView
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


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'users/home.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context