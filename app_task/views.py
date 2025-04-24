from django.shortcuts import render, redirect
from app_struct.models import Company, Division, License, Facility, Employee
from app_econ.models import Project

# Create your views here.

def task_add_obj(type, id):
    if type == 'company':
        obj = Company.objects.get(id=id)
    if type == 'division':
        obj = Division.objects.get(id=id)
    if type == 'license':
        obj = License.objects.get(id=id)
    if type == 'facility':
        obj = Facility.objects.get(id=id)
    if type == 'project':
        obj = Project.objects.get(id=id)
    return obj
def task_add(request, type, id, tid):
    type = type
    id = id
    obj = task_add_obj(type, id)
    employes = Employee.objects.all()

    # Проверка: если tid > -1, то получаем задачу
    # task = Task.objects.get(id=tid)
    # иначе task = tid

    if request.method == "GET":
        context = {
            'newtask': True,
            'type': type,
            'id': id,
            'obj': obj,
            'employes': employes,
        }
        return render(request, 'app_task/task.html', context=context)
    
    else:
        print('type', type, 'id', id)

        # from_url = request.META.get('HTTP_REFERER')
        # from_url_l = from_url.split('/')

        #     if from_url_l[-3] == 'company':
        #         return redirect('company', from_url_l[-2])
        #     if from_url_l[-3] == 'division':
        #         return redirect('division', from_url_l[-4], from_url_l[-2])
        #     if from_url_l[-3] == 'facility':
        #         return redirect('facility', from_url_l[-6], from_url_l[-4], from_url_l[-2])
        #     if from_url_l[-3] == 'license':
        #         return redirect('license', from_url_l[-2])
        #     if from_url_l[-3] == 'project':
        #         return redirect('project', from_url_l[-2])

        return redirect((type), id)