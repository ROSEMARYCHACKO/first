# Generated by Django 4.1.3 on 2022-11-20 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_soil_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='soil_test',
            name='flag',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
