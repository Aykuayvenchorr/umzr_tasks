from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from app_struct.models import *
from app_struct.forms import *



# Create your views here.
def index(request):
    return render(request, 'app_struct/index.html')


def signin(request):    
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST':     
        if form.is_valid():
            # username = request.POST["username"]
            # password = request.POST["password"]
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)   # Проверяем учетные данные
            if user is not None:
                login(request, user)                                    # Выполняем вход
                return redirect('index')                                # Перенаправляем на главную страницу
    return render(request, 'login.html', {'form': form})

@login_required(login_url="/")
def signout(request):
    logout(request)
    return redirect('index')
