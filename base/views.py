from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Task
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView,DeleteView,FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy


class LoginUser(LoginView):
    template_name = "base/login.html"
    field = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('slope')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('slope')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)

    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('slope')
        return super(RegisterPage,self).get(*args,**kwargs)


class ListPend(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self,**kwarg):
        context = super().get_context_data(**kwarg)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        value_Searched = self.request.GET.get('Search-Area') or ''
        if value_Searched:
            context['tasks'] = context['tasks'].filter(title__icontains=value_Searched)
        context['value_searched'] = value_Searched
        return context


class DetailTask(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class CreateTask(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title','description','complete'] #Incorpora_todo de mis listas
    success_url = reverse_lazy('slope')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTask,self).form_valid(form)


class UpdateTask(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('slope')


class DeleteTask(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('slope')

