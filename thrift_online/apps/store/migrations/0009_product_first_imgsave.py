# Generated by Django 3.2 on 2021-07-30 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_remove_product_first_imgsave'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='first_imgsave',
            field=models.BooleanField(default=False),
        ),
    ]
