# Generated by Django 2.2.1 on 2020-03-06 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Seller', '0005_auto_20200227_0112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginuser',
            name='address',
            field=models.TextField(blank=True, null=True, verbose_name='址地'),
        ),
    ]