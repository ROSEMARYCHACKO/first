# Generated by Django 4.1.1 on 2022-10-12 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_chat_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='user_name',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]