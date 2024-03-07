# views.py

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, TemplateView)
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse_lazy, reverse
from django.http import Http404
from django.views.generic.edit import FormMixin
from .models import Blog, Profile, Message
from .forms import SignUpForm, ProfileForm, MessageForm, BlogForm, LoginForm

class IndexView(ListView):
    model = Blog
    template_name = 'index.html'
    context_object_name = 'blogs'
    paginate_by = 5

    def get_queryset(self):
        return Blog.objects.all().order_by('-created_at')

    def get(self, request, *args, **kwargs):
        blogs = self.get_queryset()
        return render(request, self.template_name, {'blogs': blogs})

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'

    def get(self, request, *args, **kwargs):
        blog = self.get_object()
        edit_form = BlogForm(instance=blog)
        return render(request, self.template_name, {'blog': blog, 'edit_form': edit_form})

    def post(self, request, *args, **kwargs):
        blog = self.get_object()

        return self.get(request, *args, **kwargs)

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Blog creado correctamente.')
        return response

    def get_success_url(self):
        return reverse('blog_detail', kwargs={'pk': self.object.pk})


class BlogListView(ListView):
    model = Blog
    template_name = 'index.html'
    context_object_name = 'blogs'
    paginate_by = 5

    def get_queryset(self):
        return Blog.objects.all()

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        role = form.cleaned_data['role']
        user = form.save()

        if role == 'admin':
            user.is_staff = True
            user.is_superuser = True

        user.save()

        login(self.request, user)
        messages.success(self.request, '¡Registro exitoso! ¡Bienvenido!')
        return super().form_valid(form)



class LoginView(FormView):
    template_name = 'registration/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, '¡Inicio de sesión exitoso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Inicio de sesión fallido. Por favor, verifica tus credenciales.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('profile')

class ProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('about')  

    def get_object(self, queryset=None):
        if hasattr(self.request.user, 'profile'):
            return self.request.user.profile
        else:
            profile = Profile.objects.create(user=self.request.user)
            return profile

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Perfil actualizado correctamente.')
        return response


class AboutView(TemplateView):
    template_name = 'about.html'

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'about.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user.profile

class PagesView(ListView):
    model = Blog
    template_name = 'pages.html'
    context_object_name = 'blogs'
    paginate_by = 5

    def get_queryset(self):
        return Blog.objects.all()
