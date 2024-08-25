from django.db import models


class Task(models.Model):
    STATUSES_CHOICES = [
        ('New', 'New'),
        ('In_progress', 'In_progress'),
        ('Done', 'Done'),
        ('Pending', 'Pending'),
        ('Blocked', 'Blocked'),
    ]
    title = models.CharField(max_length=100, unique_for_date='created_at', verbose_name="Название")
    description = models.CharField(max_length=255, verbose_name="Описание")
    categories = models.ManyToManyField('Category')
    status = models.CharField(max_length=50, null=True, choices=STATUSES_CHOICES, default='New')
    deadline = models.DateTimeField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Задача для выполнения: {self.title}'

    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
        unique_together = ['title']


class SubTask(models.Model):
    STATUSES_CHOICES = [
        ('New', 'New'),
        ('In_progress', 'In_progress'),
        ('Done', 'Done'),
        ('Pending', 'Pending'),
        ('Blocked', 'Blocked'),
    ]

    title = models.CharField(max_length=100, verbose_name="Название подзадачи")
    description = models.CharField(max_length=255, verbose_name="Описание")
    task = models.ForeignKey('Task', null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, null=True, choices=STATUSES_CHOICES, default='New')
    deadline = models.DateTimeField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Отдельная часть основной задачи: {self.title}'

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'Subtask'
        unique_together = ['title']


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'Категория выполнения: {self.name}'

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        unique_together = ['name']


class Tag(models.Model):
    title = models.CharField(max_length=25)

    def __str__(self):
        return self.title
