# Generated by Django 3.2 on 2021-07-30 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_product_num_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='first_imgsave',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='productimage',
            name='first_imgsave',
            field=models.BooleanField(default=True),
        ),
    ]
