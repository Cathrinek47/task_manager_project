# Generated by Django 5.1 on 2024-09-03 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager_project', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='subtask',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='task',
            unique_together=set(),
        ),
    ]
