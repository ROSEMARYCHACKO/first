# Generated by Django 4.1.1 on 2022-10-02 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_products_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='count',
            field=models.IntegerField(),
        ),
    ]