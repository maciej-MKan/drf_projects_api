# Generated by Django 4.2.1 on 2023-06-01 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectuser',
            name='name',
        ),
        migrations.RemoveField(
            model_name='projectuser',
            name='surname',
        ),
        migrations.AlterField(
            model_name='projectuser',
            name='first_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='projectuser',
            name='gender',
            field=models.CharField(choices=[('Ms', 'female'), ('Mr', 'male')], max_length=10),
        ),
        migrations.AlterField(
            model_name='projectuser',
            name='last_name',
            field=models.CharField(max_length=255),
        ),
    ]
