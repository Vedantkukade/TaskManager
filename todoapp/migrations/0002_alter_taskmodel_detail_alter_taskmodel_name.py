# Generated by Django 4.1.3 on 2023-08-03 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskmodel',
            name='detail',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='taskmodel',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
