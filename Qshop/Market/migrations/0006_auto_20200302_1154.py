# Generated by Django 2.2.1 on 2020-03-02 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0005_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cart_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Seller.LoginUser', to_field='email', verbose_name='买家'),
        ),
    ]