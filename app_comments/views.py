from django.shortcuts import render
from app_struct.models import *
from app_comments.models import *
from app_econ.models import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse


struct = {
    'company': Company,
    'division': Division,
    'license': License,
    'project': Project,
    'facility': Facility
}


# Create your views here.

def comment_unchecked(request, id):
    comment = get_object_or_404(Comment, id=id)
    comment.actual = False
    comment.save()

    from_url = request.META.get('HTTP_REFERER')
    from_url_l = from_url.split('/')
    print(from_url_l)
    if from_url_l[-3] == 'company':
        return redirect('company', from_url_l[-2])
    if from_url_l[-3] == 'division':
        return redirect('division', from_url_l[-4], from_url_l[-2])
    if from_url_l[-3] == 'facility':
        return redirect('facility', from_url_l[-6], from_url_l[-4], from_url_l[-2])
    if from_url_l[-3] == 'license':
        return redirect('license', from_url_l[-2])
    if from_url_l[-3] == 'project':
        return redirect('project', from_url_l[-2])


def comment_save(request):
    user_created = request.user.id
    employee_created = Employee.objects.get(user=user_created)
    
    comment = Comment()
    name = request.POST.get('name')
    full_name = request.POST.get('full_name')
    comment.name = name
    comment.full_name = full_name
    comment.user_created = employee_created


    from_url = request.META.get('HTTP_REFERER')
    from_url_l = from_url.split('/')
    setattr(comment, from_url_l[-3], struct[from_url_l[-3]].objects.get(id=from_url_l[-2]))
    comment.save()


    uploaded_files = request.FILES.getlist('files')
    fs = FileSystemStorage()
    folder_path = 'doc'
    files_list = []

    # Save the uploaded file to the specified folder
    for file in uploaded_files:
        file_path = fs.save(folder_path + '/' + file.name, file)

        f = Document.objects.create(user_created=employee_created, file=file_path, title=file.name, from_send=f'{from_url_l[-3]}-{from_url_l[-2]}-comment-{comment.id}')
        files_list.append(str(f.id))
        comment.documents.add(f)

    comment.files_id = ', '.join(files_list)
    comment.save()

    if from_url_l[-3] == 'company':
        return redirect('company', from_url_l[-2])
    if from_url_l[-3] == 'division':
        return redirect('division', from_url_l[-4], from_url_l[-2])
    if from_url_l[-3] == 'facility':
        return redirect('facility', from_url_l[-6], from_url_l[-4], from_url_l[-2])
    if from_url_l[-3] == 'license':
        return redirect('license', from_url_l[-2])
    if from_url_l[-3] == 'project':
        return redirect('project', from_url_l[-2])


