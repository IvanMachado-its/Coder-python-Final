from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Blog, Profile, Message

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        help_text='Campo obligatorio. Ingrese una dirección de correo electrónico válida.'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }
        help_texts = {
            'username': 'Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.',
        }

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content']
        labels = {
            'title': 'Título',
            'content': 'Contenido',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'description', 'website', 'bio', 'profile_pic']
        labels = {
            'image': 'Imagen',
            'description': 'Descripción',
            'website': 'Sitio Web',
            'bio': 'Biografía',
            'profile_pic': 'Imagen de perfil',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'bio': forms.Textarea(attrs={'rows': 5}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        labels = {
            'content': 'Contenido del mensaje',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }
        
class BlogDeleteForm(forms.Form):
    confirmation = forms.BooleanField(
        required=True,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Confirmo que deseo eliminar este blog'
    )
    