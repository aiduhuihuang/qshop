# Generated by Django 2.2.1 on 2020-02-27 00:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Seller', '0003_auto_20200226_2145'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goods',
            options={'ordering': ['-id'], 'verbose_name_plural': '商品表'},
        ),
    ]
