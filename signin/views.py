from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def welcome(request):
    if request.POST.get('email'):
        request.session['email']
        return render(request, 'studentrpt.html')
    return render(request, 'welcome.html')