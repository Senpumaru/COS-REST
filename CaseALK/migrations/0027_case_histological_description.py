# Generated by Django 3.2.4 on 2021-06-30 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CaseALK', '0026_alter_case_version_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='histological_description',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='Histological Description'),
        ),
    ]
