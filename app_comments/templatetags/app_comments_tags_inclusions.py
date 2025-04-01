from django import template
from django.utils.html import format_html
from django.db.models import Q

from app_struct.models import *
from app_struct.forms import *
from app_econ.models import *
from app_comments.models import *


register = template.Library()


@register.inclusion_tag('includes/comments/block_comment.html', takes_context=True)
def block_comment(context, id): 
    comment = Comment.objects.get(id=id)
    context = {
        'user':             context['user'],
        'comment':          comment,
    }
    return context

@register.inclusion_tag('includes/comments/block_comment_add.html', takes_context=True)
def block_comment_add(context):
    context = {
        'user': context['user'],
    }
    return context