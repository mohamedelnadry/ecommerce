# Generated by Django 4.2.2 on 2023-06-20 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_cart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='products',
            new_name='product_id',
        ),
        migrations.RenameField(
            model_name='cart',
            old_name='user',
            new_name='user_id',
        ),
    ]
