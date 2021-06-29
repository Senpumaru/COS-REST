# Generated by Django 3.2.2 on 2021-06-24 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CaseALK', '0021_auto_20210623_2257'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='delivery',
            options={'verbose_name_plural': 'ST0001 Case Deliveries'},
        ),
        migrations.AlterField(
            model_name='case',
            name='version',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterModelTable(
            name='delivery',
            table='ST0001 Case Delivery',
        ),
    ]