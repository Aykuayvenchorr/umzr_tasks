from datetime import datetime

from django.shortcuts import render, redirect
from app_doc.models import Document
from app_struct.models import Company, Division, License, Facility, Employee
from app_econ.models import Project
from app_task.models import PlanCost, PlanDateEnd, PlanDateStart, Task
from django.core.files.storage import FileSystemStorage


# Create your views here.

struct = {
    'company': Company,
    'division': Division,
    'license': License,
    'project': Project,
    'facility': Facility
}


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
    # Получаем объект по type и id
    obj = task_add_obj(type, id)  # Предположительно, эта функция возвращает объект
    # print(type, id, tid)  # Для отладки

    
    # Получаем всех сотрудников
    employees = Employee.objects.all()
    
    # Проверка на tid: если tid > -1, то это существующая задача
    if int(tid) > -1:
        task = Task.objects.get(id=tid)  # Получаем задачу по id
    else:
        task = None  # Это новая задача, не найдено существующей задачи
    
    # Обработка GET-запроса
    if request.method == "GET":
        context = {
            'newtask': True if task is None else False,  # Флаг для новой задачи
            'type': type,
            'id': id,
            'obj': obj,
            'task': task,  # Если задача существует, передаем её в контекст
            'employees': employees,
        }
        return render(request, 'app_task/task.html', context=context)
    
    if request.method == "POST":
        user_created = request.user.id
        employee_created = Employee.objects.get(user=user_created)
        
        task = Task()
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        note = request.POST.get('note')
        task.name = name
        task.desc = desc
        task.note = note
        task.user_responsible = Employee.objects.get(id=request.POST.get('user_responsible'))
        task.importance = request.POST.get('importance')
        task.status = request.POST.get('status')
        task.actual = request.POST.get('actual') == 'true'  # checkbox
        task.cost_info = request.POST.get('cost_info')


        # Даты (плановые и фактические)
        dt_start = request.POST.get('dt_start') 
        dt_end = request.POST.get('dt_end')      

        fact_fin_dt = request.POST.get('fact_fin_dt')
        plan_fin_dt = request.POST.get('plan_fin_dt')
        fact_dev_dt = request.POST.get('fact_dev_dt')
        plan_dev_dt = request.POST.get('plan_dev_dt')

        # Стоимости
        fact_dev_cost = request.POST.get('fact_dev_cost')
        fact_fin_cost = request.POST.get('fact_fin_cost')
        plan_dev_cost = request.POST.get('plan_dev_cost')
        plan_fin_cost = request.POST.get('plan_fin_cost')
        

        nds = request.POST.get('nds')
        ndfl = request.POST.get('ndfl')
        task.user_created = employee_created

        obj = task_add_obj(type, id)
        from_url = request.META.get('HTTP_REFERER')
        from_url_l = from_url.split('/')
        setattr(task, type, obj)

        # Конвертация типов
        def parse_date(value):
            if value:
                try:
                    return datetime.strptime(value, "%Y-%m-%d").date()
                except ValueError:
                    return None
            return None

        def parse_float(value):
            try:
                return float(value)
            except (TypeError, ValueError):
                return None

        task.fact_fin_dt = parse_date(fact_fin_dt)
        plan_fin_dt = parse_date(plan_fin_dt)
        task.fact_dev_dt = parse_date(fact_dev_dt)
        plan_dev_dt = parse_date(plan_dev_dt)

        task.fact_dev_cost = parse_float(fact_dev_cost)
        task.fact_fin_cost = parse_float(fact_fin_cost)
        plan_dev_cost = parse_float(plan_dev_cost)
        plan_fin_cost = parse_float(plan_fin_cost)
        nds = parse_float(nds)
        ndfl = parse_float(ndfl)



        task.save()


        uploaded_files = request.FILES.getlist('files')
        fs = FileSystemStorage()
        folder_path = 'doc'
        files_list = []

        # Save the uploaded file to the specified folder
        for file in uploaded_files:
            file_path = fs.save(folder_path + '/' + file.name, file)

            f = Document.objects.create(user_created=employee_created, file=file_path, title=file.name, from_send=f'{type}-{id}-task-{task.id}')
            files_list.append(str(f.id))
            task.documents.add(f)

        # task.files_id = ', '.join(files_list)
        task.save()

        if plan_fin_dt and plan_dev_dt:
            plan_cost = PlanCost.objects.create(
                task=task,
                plan_fin_dt = parse_date(request.POST.get('plan_fin_dt')),
                plan_dev_dt = parse_date(request.POST.get('plan_dev_dt')),
                plan_fin_cost=request.POST.get('plan_fin_cost') or 0,
                plan_dev_cost=request.POST.get('plan_dev_cost') or 0,
                nds=request.POST.get('nds') or 0,
                ndfl=request.POST.get('ndfl') or 0
            )


        # Получаем значения дат из запроса
        dt_start = parse_date(request.POST.get('dt_start'))
        dt_end = parse_date(request.POST.get('dt_end'))

        # Сохраняем плановые даты начала и завершения
        plan_date_start = PlanDateStart.objects.create(
            task=task,
            dt_start=dt_start,
            user_created = Employee.objects.get(user=request.user.id))

        plan_date_end = PlanDateEnd.objects.create(
            task=task,
            dt_end=dt_end,
            user_created = Employee.objects.get(user=request.user.id)
        )



        if from_url_l[-4] == 'company':
            return redirect('company', from_url_l[-3])
        if from_url_l[-4] == 'division':
            return redirect('division', obj.company.id, from_url_l[-3])
        if from_url_l[-4] == 'facility':
            return redirect('facility', obj.license.owner.id, obj.license.id, from_url_l[-3])
        if from_url_l[-4] == 'license':
            return redirect('license', from_url_l[-3])
        if from_url_l[-4] == 'project':
            return redirect('project', from_url_l[-3])