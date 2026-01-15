from django.urls import path
from . import views

urlpatterns = [
    path('', views.board, name='board'),
    path('new/', views.create_task, name='create_task'),
    path('delete/<int:pk>/', views.delete_task, name='delete_task'),
]
