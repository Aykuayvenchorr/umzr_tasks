from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from app_comments.models import *


from app_struct.models import *
from app_struct.forms import *
from app_econ.models import *
from django.utils.html import strip_tags

from app_task.models import Task



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
    comments = Comment.objects.filter(company=company)
    tasks = Task.objects.filter(company=company, parent__isnull=True)

    context = {
        'company': company,
        'comments': comments,
        'tasks': tasks
    }
    return render(request, 'app_struct/company.html', context=context)

def company_save(request, id):
    if request.method == "POST":
        company = get_object_or_404(Company, id=id)
        note = request.POST.get('note', company.note)
        contacts = request.POST.get('contacts', company.contacts)
        company.note = note
        company.contacts = contacts
        company.save()
        return redirect(('company'), id)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def subcompanies(request, id):
    company = Company.objects.get(id=id)
    subcompanies = company.subcompany.filter(actual=True).order_by('title')
    context = {
        'company': company,
        'subcompanies': subcompanies,
    }
    return render(request, 'app_struct/companies_sub.html', context=context)


def licenses(request, id):
    company = Company.objects.get(id=id)    
    context = {
        'company': company,        
    }
    return render(request, 'app_struct/licenses.html', context=context)

def license(request, id):
    license = License.objects.get(id=id)
    comments = Comment.objects.filter(license=license)

    context = {
        'license': license,        
        'comments': comments,        
    }
    return render(request, 'app_struct/license.html', context=context)

def license_save(request, id, id_lic):
    if request.method == "POST":
        license = License.objects.get(id=id_lic)
        note = request.POST.get('note', license.note)
        license.note = note
        license.save()
        return redirect(('license'), id_lic)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def license_facilities(request, id, id_lic):
    company = Company.objects.get(id=id)    
    license = License.objects.get(id=id_lic)    
    context = {        
        'company': company,
        'license': license,        
    }
    return render(request, 'app_struct/license_facilities.html', context=context)


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
    comments = Comment.objects.filter(facility=facility)

    context = {        
        'company': company,
        'license': license,
        'facility': facility,       
        'comments': comments,       
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


def divisions(request, id):
    company = Company.objects.get(id=id)    
    context = {
        'company': company,        
    }
    return render(request, 'app_struct/divisions.html', context=context)

def division(request, id, id_div):
    company = Company.objects.get(id=id)   
    division = Division.objects.get(id=id_div)
    comments = Comment.objects.filter(division=division)


    context = {
        'company': company,  
        'division': division,   
        'comments': comments 
    }
    return render(request, 'app_struct/division.html', context=context)

def subdivisions(request, id, id_div):
    company = Company.objects.get(id=id)
    division = Division.objects.get(id=id_div)
    context = {
        'company': company,
        'division': division,
    }
    return render(request, 'app_struct/divisions_sub.html', context=context)

def division_projects(request, id, id_div):
    company = Company.objects.get(id=id)
    division = Division.objects.get(id=id_div)
    context = {
        'company': company,
        'division': division,        
    }
    return render(request, 'app_struct/division_projects.html', context=context)


def license_projects(request, id, id_lic):
    company = Company.objects.get(id=id)
    license = License.objects.get(id=id_lic)
    context = {
        'company': company,
        'license': license,        
    }
    return render(request, 'app_struct/license_projects.html', context=context)



def project_div (request, id, id_div, id_pr):
    company = Company.objects.get(id=id)
    division = Division.objects.get(id=id_div)
    project = Project.objects.get(id=id_pr)
    comments = Comment.objects.filter(project=project)

    context = {
        'company': company,
        'division': division,
        'project': project,   
        'comments': comments,   
     }
    return render(request, 'app_struct/project.html', context=context)







def save_div(request, id, id_div):
    if request.method == "POST":
        # company = get_object_or_404(Company, id=id)
        division = get_object_or_404(Division, id=id_div)
        note = request.POST.get('note', division.note)
        contacts = request.POST.get('contacts', division.contacts)
        division.note = note
        division.contacts = contacts
        division.save()
        return redirect(('division'), id, id_div)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def save_facility(request, id, id_lic, id_fc):
    if request.method == "POST":
        facility = get_object_or_404(Facility, id=id_fc)
        note = request.POST.get('note', facility.note)
        facility.note = note
        facility.save()
        return redirect(('facility'), id, id_lic, id_fc)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})