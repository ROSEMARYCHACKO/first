# Generated by Django 4.1.1 on 2022-09-25 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_products_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='image',
            field=models.ImageField(default=0, upload_to='images/'),
            preserve_default=False,
        ),
    ]