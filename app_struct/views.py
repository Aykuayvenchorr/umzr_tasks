from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from app_struct.models import *
from app_struct.forms import *
from app_econ.models import *



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


def companies(request):
    return render(request, 'app_struct/companies.html')

def company(request, id):
    company = Company.objects.get(id=id)
    context = {
        'company': company,
    }
    return render(request, 'app_struct/company.html', context=context)

def subcompanies(request, id):
    company = Company.objects.get(id=id)
    subcompanies = company.subcompany.filter(actual=True).order_by('title')
    context = {
        'company': company,
        'subcompanies': subcompanies,
    }
    return render(request, 'app_struct/subcompanies.html', context=context)

def divisions(request, id):
    company = Company.objects.get(id=id)    
    context = {
        'company': company,        
    }
    return render(request, 'app_struct/divisions.html', context=context)

def division(request, id, id_div):
    company = Company.objects.get(id=id)   
    division = Division.objects.get(id=id_div)

    context = {
        'company': company,  
        'division': division,    
    }
    return render(request, 'app_struct/division.html', context=context)

def subdivisions(request, id, id_div):
    company = Company.objects.get(id=id)
    division = Division.objects.get(id=id_div)
    context = {
        'company': company,
        'division': division,
    }
    return render(request, 'app_struct/subdivisions.html', context=context)

def licenses(request, id):
    company = Company.objects.get(id=id)    
    context = {
        'company': company,        
    }
    return render(request, 'app_struct/licenses.html', context=context)

def license(request, id, id_lic):
    company = Company.objects.get(id=id)
    license = License.objects.get(id=id_lic)
    context = {
        'company': company,
        'license': license,        
    }
    return render(request, 'app_struct/license.html', context=context)

def facilities(request, id, id_lic):
    company = Company.objects.get(id=id)    
    license = License.objects.get(id=id_lic)    
    context = {        
        'company': company,
        'license': license,        
    }
    return render(request, 'app_struct/facilities.html', context=context)

def facility(request, id, id_lic, id_fc):
    company = Company.objects.get(id=id)    
    license = License.objects.get(id=id_lic)
    facility = Facility.objects.get(id=id_fc)
    context = {        
        'company': company,
        'license': license,
        'facility': facility,       
    }
    return render(request, 'app_struct/facility.html', context=context)

def subfacilities(request, id, id_lic, id_fc):
    company = Company.objects.get(id=id)
    license = License.objects.get(id=id_lic)
    facility = Facility.objects.get(id=id_fc)
    context = {
        'company': company,
        'license': license,
        'facility': facility,
    }
    return render(request, 'app_struct/subfacilities.html', context=context)

def projects(request, id, id_lic):
    company = Company.objects.get(id=id)
    license = License.objects.get(id=id_lic)
    context = {
        'company': company,
        'license': license,        
    }
    return render(request, 'app_struct/projects.html', context=context)

def project(request, id, id_lic, id_pr):
    company = Company.objects.get(id=id)
    license = License.objects.get(id=id_lic)
    project = Project.objects.get(id=id_pr)
    context = {
        'company': company,
        'license': license,
        'project': project,        
    }
    return render(request, 'app_struct/project.html', context=context)