# Generated by Django 4.0.1 on 2024-07-23 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cymaticsapp', '0026_alter_project_client'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='client',
        ),
    ]
