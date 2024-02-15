from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class AuthForm(AuthenticationForm):
    class Meta:
        model = User
        fields = 'username', 'password'


class RegisterForm(UserCreationForm):
    class Meta:
        model = User

        fields = ('username',
                  'email',
                  'is_staff',
                  'password1',
                  'password2')
