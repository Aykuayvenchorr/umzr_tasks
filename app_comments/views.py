from django.shortcuts import render
from app_struct.models import *
from app_comments.models import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

# Create your views here.
def comments_company(request, id):
    company = get_object_or_404(Company, id=id)
    comments = Comment.objects.filter(company=company)
    context = {
        'company': company, 
        'comments': comments
    }
    return render(request, 'app_struct/company.html', context=context)

