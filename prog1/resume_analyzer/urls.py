from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='analyzer_index'),
    path('analyze/', views.analyze, name='analyze'),
    path('result/<int:result_id>/', views.result, name='result'),
    path('history/', views.history, name='history'),
]
