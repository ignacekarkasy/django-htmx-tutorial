from django.shortcuts import render

def home_view(request, *args, **kwargs):
    title = "Welcome to django"
    return render(request, 'base.html', {'title': title})