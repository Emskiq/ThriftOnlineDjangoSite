# Generated by Django 3.2 on 2021-07-21 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='place',
            new_name='city',
        ),
        migrations.AddField(
            model_name='order',
            name='office',
            field=models.CharField(default='', max_length=120),
        ),
    ]
