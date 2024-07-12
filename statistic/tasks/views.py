from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Task
from .forms import TaskForm

@login_required
def task_list(request):
    # Получаем все задачи, назначенные текущему пользователю
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def task_detail(request, pk):
    # Получаем задачу по её primary key (pk)
    task = get_object_or_404(Task, pk=pk)

    # Если была отправлена форма и кнопка "Взять в работу" нажата
    if request.method == 'POST' and 'start_working' in request.POST:
        # Вызываем метод start_working модели Task для начала работы над задачей
        task.start_working(request.user)
        return redirect('task_detail', pk=pk)  # Перенаправляем на страницу деталей задачи

    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_to = request.user  # Назначаем текущего пользователя ответственным за задачу
            task.save()
            return redirect('task_detail', pk=task.pk)  # Перенаправляем на страницу деталей созданной задачи
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_edit(request, pk):
    # Получаем задачу по её primary key (pk)
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()  # Сохраняем отредактированную форму задачи
            return redirect('task_detail', pk=pk)  # Перенаправляем на страницу деталей задачи
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    # Получаем задачу по её primary key (pk)
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()  # Удаляем задачу
        return redirect('task_list')  # Перенаправляем на список задач
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@login_required
def task_complete(request, pk):
    # Получаем задачу по её primary key (pk)
    task = get_object_or_404(Task, pk=pk)
    task.status = 'done'  # Устанавливаем статус задачи как завершённая
    task.completion_time = timezone.now()  # Устанавливаем время завершения задачи как текущее
    task.save()  # Сохраняем изменения
    return redirect('task_list')  # Перенаправляем на список задач
