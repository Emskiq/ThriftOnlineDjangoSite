# Generated by Django 3.2 on 2021-07-30 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20210730_2208'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='first_imgsave',
        ),
    ]
