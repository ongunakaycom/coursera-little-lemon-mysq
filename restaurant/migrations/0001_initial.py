# Generated by Django 5.1.5 on 2025-02-01 02:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('description', models.TextField(blank=True, max_length=1000)),
                ('category', models.CharField(choices=[('ST', 'Starter'), ('MN', 'Main Course'), ('DS', 'Dessert'), ('BE', 'Beverage')], default='MN', max_length=2)),
                ('available', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Menu Item',
                'verbose_name_plural': 'Menu Items',
                'ordering': ['category', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation_time', models.TimeField()),
                ('reservation_date', models.DateField()),
                ('guests', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('seats', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='Guest', max_length=100, verbose_name='Guest Name')),
                ('reservation_date', models.DateField()),
                ('reservation_time', models.CharField(choices=[('10:00', '10:00 AM'), ('10:30', '10:30 AM'), ('11:00', '11:00 AM'), ('11:30', '11:30 AM'), ('12:00', '12:00 PM'), ('12:30', '12:30 PM'), ('13:00', '1:00 PM'), ('13:30', '1:30 PM'), ('14:00', '2:00 PM'), ('14:30', '2:30 PM'), ('15:00', '3:00 PM'), ('18:30', '6:30 PM'), ('21:30', '9:30 PM')], max_length=5, verbose_name='Time Slot')),
                ('guests', models.PositiveIntegerField(default=1, verbose_name='Number of Guests')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookings', to=settings.AUTH_USER_MODEL)),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='restaurant.table', verbose_name='Table Number')),
            ],
            options={
                'ordering': ['-reservation_date', '-reservation_time'],
                'unique_together': {('reservation_date', 'reservation_time', 'table')},
            },
        ),
    ]
