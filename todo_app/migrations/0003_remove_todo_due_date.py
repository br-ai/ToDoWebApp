# Generated by Django 4.1.1 on 2022-09-11 00:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0002_todo_delete_todoitem_delete_todolist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='due_date',
        ),
    ]
