# Generated by Django 3.2 on 2021-07-30 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_product_first_imgsave'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='first_imgsave',
            field=models.BooleanField(default=True),
        ),
    ]