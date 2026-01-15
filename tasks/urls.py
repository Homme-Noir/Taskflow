from django.urls import path
from . import views

urlpatterns = [
    path('', views.board, name='board'),
    path('signup/', views.signup, name='signup'),
    path('new/', views.create_task, name='create_task'),
    path('edit/<int:pk>/', views.update_task, name='update_task'),
    path('delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('status/<int:pk>/<str:status>/', views.change_status, name='change_status'),
]
