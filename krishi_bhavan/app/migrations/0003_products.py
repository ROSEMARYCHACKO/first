# Generated by Django 4.1.1 on 2022-09-25 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_rename_user_name_service_provider_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=250)),
                ('rate', models.CharField(max_length=50)),
                ('count', models.CharField(max_length=100)),
            ],
        ),
    ]
