from django import template

from app_task.models import *


register = template.Library()


@register.inclusion_tag('includes/tasks/block_task.html', takes_context=True)
def block_task(context, task_id, type, type_id): 
    task = Task.objects.get(id=task_id)
    plandatestart = PlanDateStart.objects.filter(task=task, actual=True)
    plandateend = PlanDateEnd.objects.filter(task=task, actual=True)

    context = {
        'user':          context['user'],
        'task':          task,
        'plandatestart': plandatestart,
        'plandateend': plandateend,
        'type': type,
        'type_id': type_id
    }
    return context
