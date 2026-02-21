from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('email','phone_number', 'location', 'avatar', 'date_birth')
        

class ProfileForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'phone_number', 'location', 'avatar', 'date_birth' , 'bio')
