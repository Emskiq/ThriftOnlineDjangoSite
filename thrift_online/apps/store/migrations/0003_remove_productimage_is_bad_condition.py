# Generated by Django 3.2 on 2021-05-28 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_productimage_is_bad_condition'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='is_bad_condition',
        ),
    ]
