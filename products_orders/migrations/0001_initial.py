# Generated by Django 4.0 on 2022-01-03 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products_carts', '0002_cart_subtotal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=120)),
                ('status', models.CharField(choices=[('created', 'Created'), ('paid', 'Paid'), ('shipped', 'Shipped'), ('refunded', 'Refunded')], default='created', max_length=120)),
                ('shipping_total', models.DecimalField(decimal_places=2, default=5.99, max_digits=100)),
                ('total', models.DecimalField(decimal_places=2, default=5.99, max_digits=100)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products_carts.cart')),
            ],
        ),
    ]
