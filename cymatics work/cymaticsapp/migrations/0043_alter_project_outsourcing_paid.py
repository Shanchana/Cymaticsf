# Generated by Django 4.0.1 on 2024-08-01 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cymaticsapp', '0042_alter_project_address_alter_project_expenses_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='outsourcing_paid',
            field=models.BooleanField(default=False),
        ),
    ]
