from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from .models import Profile


class ProfileUpdateForm(forms.ModelForm):
    """Форма редактирования профиля в личном кабинете."""
    class Meta:
        model = Profile
        fields = ["avatar", "bio"]


class SimpleRegisterForm(forms.Form):
    """Простая форма регистрации с кастомными подписями и стилями."""

    username = forms.CharField(
        label="Логин",
        help_text="Разрешены буквы, цифры и символы @/./+/-/_ .",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите логин",
            }
        ),
    )

    email = forms.EmailField(
        label="Email",
        help_text="Введите действительный адрес электронной почты.",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите email",
            }
        ),
    )

    password = forms.CharField(
        label="Пароль",
        help_text="Пароль должен содержать минимум 8 символов и не быть полностью цифровым.",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите пароль",
            }
        ),
    )

    # --- проверки полей ---

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise ValidationError("Пользователь с таким логином уже существует.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email

    def clean_password(self):
        password = self.cleaned_data["password"]
        validate_password(password)
        return password

    # --- создание пользователя ---

    def save(self):
        username = self.cleaned_data["username"]
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        return user
