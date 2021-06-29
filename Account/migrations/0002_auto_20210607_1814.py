# Generated by Django 3.2.2 on 2021-06-07 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceuser',
            name='ST0001_allow',
            field=models.BooleanField(default=False, help_text='Gives access to ST0001 application.', verbose_name='Application for IHC:ALK cases'),
        ),
        migrations.AddField(
            model_name='serviceuser',
            name='ST0002_allow',
            field=models.BooleanField(default=False, help_text='Gives access to ST0002 application.', verbose_name='Application for IHC:PDL1 cases'),
        ),
    ]