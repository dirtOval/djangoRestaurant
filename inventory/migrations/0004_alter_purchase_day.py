# Generated by Django 3.2.8 on 2021-11-30 01:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_alter_purchase_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='day',
            field=models.ForeignKey(default=24, on_delete=django.db.models.deletion.CASCADE, to='inventory.revenueday'),
        ),
    ]