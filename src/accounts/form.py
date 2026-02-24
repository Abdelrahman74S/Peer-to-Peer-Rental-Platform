from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('email','phone_number', 'location', 'avatar', 'date_birth')
        

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
        'email',
        'username',
        'phone_number',
        'location',
        'avatar',
        'date_birth',
        'bio',
        'facebook_url',
        'whatsapp_number',
        'preferred_language',
)
        input_classes = 'w-full px-4 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition duration-200 bg-white'
        
        readonly_classes = 'w-full px-4 py-2 rounded-lg border border-slate-200 bg-slate-50 text-slate-500 cursor-not-allowed'

        widgets = {
            'email': forms.EmailInput(attrs={'class': input_classes, 'placeholder': 'example@mail.com'}),
            'username': forms.TextInput(attrs={'class': input_classes}),
            'phone_number': forms.TextInput(attrs={'class': input_classes, 'placeholder': '01xxxxxxxxx'}),
            'whatsapp_number': forms.TextInput(attrs={'class': input_classes, 'placeholder': '201xxxxxxxxx'}),
            'facebook_url': forms.URLInput(attrs={'class': input_classes, 'placeholder': 'https://facebook.com/username'}),
            'location': forms.TextInput(attrs={'class': input_classes}),
            'bio': forms.Textarea(attrs={'class': input_classes, 'rows': 3}),
            'date_birth': forms.DateInput(attrs={'class': input_classes, 'type': 'date'}),
            'preferred_language': forms.Select(attrs={'class': input_classes}),
            'avatar': forms.FileInput(attrs={'class': 'block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'}),
            
            'rating': forms.NumberInput(attrs={'class': readonly_classes, 'readonly': 'readonly'}),
            'reviews_count': forms.NumberInput(attrs={'class': readonly_classes, 'readonly': 'readonly'}),
            'items_rented_count': forms.NumberInput(attrs={'class': readonly_classes, 'readonly': 'readonly'}),
            'items_listed_count': forms.NumberInput(attrs={'class': readonly_classes, 'readonly': 'readonly'}),
        }
