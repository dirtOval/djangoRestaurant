# Generated by Django 3.2.8 on 2021-11-30 02:32

from django.db import migrations, models
import django.db.models.deletion
import inventory.models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_alter_purchase_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='revenueday',
            name='cost',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='day',
            field=models.ForeignKey(default=inventory.models.Purchase.get_default, on_delete=django.db.models.deletion.CASCADE, to='inventory.revenueday'),
        ),
    ]
