# Generated by Django 4.1.1 on 2022-10-12 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_chat_user_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='product_id',
        ),
    ]
