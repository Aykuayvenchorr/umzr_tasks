from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from app_econ.models import *
from app_struct.models import *

# Create your views here.
def project(request, id):
    project = Project.objects.get(id=id)
    context = {
        'project': project,   
    }
    return render(request, 'app_econ/project.html', context=context)

def save_project(request, id):
    if request.method == "POST":
        project = get_object_or_404(Project, id=id)
        note = request.POST.get('note', project.note)
        contacts = request.POST.get('contacts', project.contacts)
        project.note = note
        project.contacts = contacts
        project.save()
        return redirect(('project'), id)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})