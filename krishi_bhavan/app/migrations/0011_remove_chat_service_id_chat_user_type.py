# Generated by Django 4.1.1 on 2022-10-12 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_chat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='service_id',
        ),
        migrations.AddField(
            model_name='chat',
            name='user_type',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]
