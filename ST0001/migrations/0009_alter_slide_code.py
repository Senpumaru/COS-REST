# Generated by Django 3.2.5 on 2021-09-11 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ST0001', '0008_alter_slide_information'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slide',
            name='code',
            field=models.CharField(blank=True, error_messages={'unique': 'Эти коды для МП уже существуют.'}, max_length=20, null=True, unique=True, verbose_name='Slide Code (New)'),
        ),
    ]