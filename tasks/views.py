from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from tasks.models import TodoItem
from tasks.forms import TodoItemForm
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse
from django.contrib import messages


@login_required
def index(request):
    return HttpResponse("Примитивный ответ из приложения tasks")


def complete_task(request, uid):
    task = TodoItem.objects.get(pk=uid)
    task.is_completed = True
    task.save()
    return HttpResponse('OK')


def delete_task(request, uid):
    task = TodoItem.objects.get(pk=uid)
    task.delete()
    messages.success(request, 'Задача удалена')
    return redirect(reverse('tasks:list'))


class TaskListView(LoginRequiredMixin, ListView):
    model = TodoItem
    context_object_name = 'tasks'
    template_name = 'tasks/list.html'

    def get_queryset(self):
        user = self.request.user
        return user.tasks.all()


class TaskCreateView(View):
    def create_render(self, request, form):
        return render(request, 'tasks/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = TodoItemForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.save()
            return redirect(reverse('tasks:list'))

        return self.create_render(request, form)

    def get(self, request, *args, **kwargs):
        form = TodoItemForm
        return self.create_render(request, form)


class TaskDetailsView(DetailView):
    model = TodoItem
    template_name = 'tasks/details.html'


class TaskEditView(LoginRequiredMixin, View):
    def create_render(self, request, form, task):
        return render(request, 'tasks/edit.html', {'form': form, 'task': task})

    def post(self, request, pk, *args, **kwargs):
        task = TodoItem.objects.get(id=pk)
        form = TodoItemForm(request.POST, instance=task)
        if form.is_valid():
            updated_task = form.save(commit=False)
            updated_task.owner = request.user
            updated_task.save()
            return redirect(reverse('tasks:list'))

        return self.create_render(request, form, task)

    def get(self, request, pk, *args, **kwargs):
        task = TodoItem.objects.get(id=pk)
        form = TodoItemForm(instance=task)
        return self.create_render(request, form, task)
