from django.shortcuts import render, redirect
from django.http import HttpResponse


def home(request):
    return render(request, "home.html")

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']
        address = request.POST['address']
        email = request.POST['email']
        return render(request, "output.html", {'NAME': name, 'PASSWORD': password, 'ADDRESS': address, 'EMAIL': email})
    return redirect('/')