# Generated by Django 3.2 on 2021-06-06 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0004_product_num_available'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=120)),
                ('last_name', models.CharField(max_length=120)),
                ('email', models.CharField(max_length=120)),
                ('address', models.CharField(max_length=120)),
                ('zip_code', models.CharField(max_length=120)),
                ('place', models.CharField(max_length=120)),
                ('phone', models.CharField(max_length=120)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('paid', models.BooleanField(default=False)),
                ('paid_amount', models.FloatField(blank=True, null=True)),
                ('used_coupon', models.CharField(blank=True, max_length=50, null=True)),
                ('payment_intent', models.CharField(max_length=255)),
                ('shipped_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('ordered', 'Ordered'), ('delivered', 'Delivered'), ('arrived', 'Arrived')], default='ordered', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('quantity', models.IntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item', to='order.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='items', to='store.product')),
            ],
        ),
    ]
