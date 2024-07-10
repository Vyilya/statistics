

from django import forms
from django.contrib.auth.models import User
from .models import Task

class TaskForm(forms.ModelForm):
    title = forms.CharField(label='Название задачи')
    description = forms.CharField(label='Описание', widget=forms.Textarea)
    assigned_to = forms.ModelChoiceField(label='Назначено на', queryset=User.objects.all())
    due_date = forms.DateField(label='Срок выполнения', widget=forms.DateInput(attrs={'type': 'date'}))
    status = forms.ChoiceField(label='Статус', choices=Task.STATUS_CHOICES)

    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'due_date', 'status']
