from django.contrib import admin
from django.urls import path, include
from My_App import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('register', views.register),
    path('analyzer/', include('resume_analyzer.urls')),
]
