# Generated by Django 4.0.1 on 2024-07-31 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cymaticsapp', '0033_rename_income_income_project_income'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='code',
            field=models.TextField(unique=True),
        ),
    ]
