# Generated by Django 4.0.1 on 2024-07-17 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='clients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('company', models.CharField(max_length=100)),
                ('number', models.IntegerField()),
                ('email', models.EmailField(max_length=100)),
                ('img', models.ImageField(upload_to='media')),
            ],
        ),
    ]
