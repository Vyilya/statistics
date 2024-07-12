from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'К выполнению'),
        ('in_progress', 'В процессе'),
        ('done', 'Завершено')
    ]

    title = models.CharField('Название задачи', max_length=255)
    description = models.TextField('Описание')
    assigned_to = models.ForeignKey(User, verbose_name='Назначено на', on_delete=models.CASCADE)
    due_date = models.DateField('Срок выполнения')
    due_time = models.TimeField('Время выполнения', default='00:00:00')
    status = models.CharField('Статус', max_length=50, choices=STATUS_CHOICES, default='todo')
    completion_time = models.DateTimeField('Время завершения', null=True, blank=True)
    start_time = models.DateTimeField('Время начала работы', null=True, blank=True)
    in_progress_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='in_progress_tasks')

    def __str__(self):
        return self.title

    def start_working(self, user):
        # Метод для начала работы над задачей
        self.start_time = timezone.now()  # Устанавливаем текущее время начала работы
        self.in_progress_by = user  # Указываем пользователя, который начал работу
        self.status = 'in_progress'  # Меняем статус задачи на "В процессе"
        self.save()  # Сохраняем изменения в базе данных

    def format_timedelta(self, td):
        # Метод для форматирования timedelta в строку с указанием дней, часов и минут
        days = td.days
        hours, remainder = divmod(td.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if days > 0:
            return f'{days} дней, {hours} часов, {minutes} минут'
        elif hours > 0:
            return f'{hours} часов, {minutes} минут'
        elif minutes > 0:
            return f'{minutes} минут'
        else:
            return f'{seconds} секунд'

    def report_time_spent(self):
        # Метод для расчёта времени, затраченного на задачу
        if self.completion_time and self.start_time:
            start_time_aware = timezone.localtime(self.start_time, timezone.get_current_timezone())
            completion_time_aware = timezone.localtime(self.completion_time, timezone.get_current_timezone())
            time_spent = completion_time_aware - start_time_aware
            return self.format_timedelta(time_spent)
        return ""

    def remaining_time(self):
        # Метод для расчёта оставшегося времени до завершения задачи
        if self.status in ['todo', 'in_progress'] and self.due_date and self.due_time:
            now = timezone.localtime(timezone.now(), timezone.get_current_timezone())
            due_datetime = timezone.make_aware(timezone.datetime.combine(self.due_date, self.due_time))

            if self.status == 'todo':
                remaining = due_datetime - now
            elif self.status == 'in_progress':
                remaining = due_datetime - self.start_time

            return self.format_timedelta(remaining)

        return ""

    def time_spent(self):
        # Метод для расчёта общего времени, затраченного на задачу
        if self.completion_time and self.start_time:
            due_datetime = timezone.make_aware(timezone.datetime.combine(self.due_date, self.due_time))
            completion_time_aware = timezone.localtime(self.completion_time, timezone.get_current_timezone())
            time_spent = completion_time_aware - due_datetime
            return time_spent
        return None
