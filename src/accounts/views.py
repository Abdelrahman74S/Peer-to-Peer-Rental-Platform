from django.shortcuts import render ,redirect
from django.urls import reverse
from .models import Profile
from .form import CustomUserCreationForm, ProfileForm
from django.contrib.auth import login
from django.views.generic import ListView , DetailView , CreateView , UpdateView , DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView , LogoutView
# Create your views here.

class RegisterView(CreateView):
    model = Profile
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    
    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    
class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    success_url = 'accounts:profile'
    
class UserLogoutView(LogoutView):
    template_name = 'accounts/logout.html'
    next_page = 'accounts:login'
    
class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile.html'
    context_object_name = 'profile'
    
class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/edit_profile.html'
    success_url = 'accounts:profile'