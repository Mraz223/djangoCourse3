from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class SimpleRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ЛОГИН
        self.fields["username"].label = "Логин"
        self.fields["username"].help_text = "Разрешены буквы, цифры и символы @/./+/-/_ ."
        self.fields["username"].error_messages["unique"] = "Пользователь с таким логином уже существует."

        # EMAIL
        self.fields["email"].label = "Email"
        self.fields["email"].error_messages["required"] = "Это поле обязательно."

        # ПАРОЛЬ
        self.fields["password1"].label = "Пароль"
        self.fields["password1"].help_text = (
            "Пароль должен содержать минимум 8 символов "
            "и не быть полностью цифровым."
        )
        self.fields["password1"].error_messages["required"] = "Это поле обязательно."

        # ПОДТВЕРЖДЕНИЕ ПАРОЛЯ
        self.fields["password2"].label = "Подтверждение пароля"
        self.fields["password2"].help_text = "Введите тот же пароль ещё раз."
        self.fields["password2"].error_messages["required"] = "Это поле обязательно."


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "bio"]
