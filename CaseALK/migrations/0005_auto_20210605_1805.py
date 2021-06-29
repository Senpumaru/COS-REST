# Generated by Django 3.2.2 on 2021-06-05 15:05

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CaseALK', '0004_auto_20210604_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='institution_code',
            field=models.CharField(blank=True, choices=[(0, 'Не указан'), (328112, 'УЗ «Гомельский областной клинический онкологический диспансер»'), (328044, 'УЗ «Витебский областной клинический онкологический диспансер»'), (328043, 'УЗ «Могилёвский областной онкологический диспансер»'), (327933, 'УЗ «Минский городской клинический онкологический диспансер»'), (327932, 'РНПЦ ОМР им. Н.Н. Александрова')], default='Не указан', max_length=80, null=True, verbose_name='Institution code'),
        ),
        migrations.AlterField(
            model_name='case',
            name='block_number',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, default='#####-##/##', max_length=20), default=list, help_text='Example: #####-##/##, #####-##/##', null=True, size=None, verbose_name='Block №'),
        ),
        migrations.AlterField(
            model_name='case',
            name='slide_number',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(default='#####-##/##', max_length=20), blank=True, default=list, help_text='Example: #####-##/##, #####-##/##', null=True, size=None, verbose_name='Slide №'),
        ),
        migrations.AlterUniqueTogether(
            name='case',
            unique_together={('personal_number', 'institution_code')},
        ),
        migrations.RemoveField(
            model_name='case',
            name='institution',
        ),
    ]
