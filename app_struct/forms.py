from django.contrib.auth.forms import AuthenticationForm
from django import forms


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username',
                               min_length = 2,
                               max_length = 17, 
                               # message kwarg is only usable in models, yet,
                               #it doesn't spawn error here.
                               #validators=[RegexValidator(regex=NME, message="In-approperiate number!")], 
                               required = True,
                               #Errors dictionary 
                               error_messages={'required': 'Укажите Ваше имя пользователя',
                                               'min_length':'Слишком короткое имя пользователя. Должно быть более 2 символов',
                                               'min_length':'Слишком короткое имя пользователя. Должно быть менее 17 символов',
                                               'invalid':'Неверное имя пользователя'}, 
                               #Similar to default you pass in model
                               initial = 'username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)