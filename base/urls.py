from django.urls import path
from .views import ListPend,DetailTask, CreateTask, UpdateTask,DeleteTask,LoginUser,RegisterPage
from django.contrib.auth.views import LogoutView

urlpatterns = [path('',ListPend.as_view(), name= 'slope'),
               path('login/',LoginUser.as_view(), name= 'login'),
               path('register/',RegisterPage.as_view(), name= 'register'),
               path('logout/', LogoutView.as_view(next_page='login'), name= 'logout'),
               path('task/<int:pk>',DetailTask.as_view(), name= 'task'),
               path('create-task/',CreateTask.as_view(), name= 'create-task'),
               path('update-task/<int:pk>',UpdateTask.as_view(), name= 'update-task'),
               path('delete-task/<int:pk>',DeleteTask.as_view(), name= 'delete-task')]