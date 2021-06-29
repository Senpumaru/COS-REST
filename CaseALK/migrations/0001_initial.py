# Generated by Django 3.2.2 on 2021-06-03 13:20

import datetime
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('date_of_registration', models.DateField(default=datetime.date.today, null=True)),
                ('personal_number', models.CharField(max_length=20, null=True, unique=True, verbose_name='Personal ID')),
                ('region', models.CharField(blank=True, default='Не указан', max_length=20, null=True, verbose_name='Region')),
                ('block_number', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, default='00000/00', max_length=20), default=list, help_text='Пример заполнения: 00001/00, 00002/00', null=True, size=None, verbose_name='Block №')),
                ('block_amount', models.PositiveIntegerField(default=1, null=True, verbose_name='Blocks')),
                ('slide_number', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(default='00000/00', max_length=20), blank=True, default=list, help_text='Пример заполнения: 00001/00, 00002/00', null=True, size=None, verbose_name='Slide №')),
                ('slide_amount', models.PositiveIntegerField(blank=True, default=1, null=True, verbose_name='Slides')),
                ('diagnosis', models.CharField(blank=True, default='Не указан', max_length=50, null=True, verbose_name='Diagnosis')),
                ('doctor_sender', models.CharField(blank=True, default='Не указан', max_length=50, null=True, verbose_name='Doctor (Sender)')),
                ('date_of_response', models.DateField(blank=True, null=True)),
                ('date_of_delivery', models.DateField(blank=True, null=True)),
                ('micro_desc', models.TextField(blank=True, default='Нет описания', max_length=500, null=True, verbose_name='Microscopic Description')),
                ('case_conclusion', models.TextField(blank=True, choices=[('Нет заключения', 'Нет заключения'), ('Гранулярность не определяется', 'Гранулярное цитоплазматическое окрашивание\n        опухолевых клеток высокой интенсивности не определяется'), ('Окрашивание высокой интенсивности', 'В большинстве опухолевых клеток определяется\n        гранулярное цитоплазматическое окрашивание высокой интенсивности')], default='Нет заключения', max_length=280, null=True, verbose_name='Conclusion')),
                ('clin_interpretation', models.CharField(blank=True, choices=[('Не указано', 'Не указано'), ('ALK-Positive', 'ALK Позитивный'), ('ALK-Negative', 'ALK Негаивный')], default='Не указано', max_length=200, null=True, verbose_name='Clinical Interpratation')),
                ('date_created', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Date created')),
                ('date_updated', models.DateField(auto_now=True, null=True, verbose_name='Date updated')),
            ],
            options={
                'verbose_name_plural': 'ALK Cases',
                'db_table': 'ALK Case',
                'ordering': ['date_of_registration'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('date_created', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Date Created')),
                ('date_updated', models.DateField(auto_now=True, null=True, verbose_name='Date Updated')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='AuthorsALK', to=settings.AUTH_USER_MODEL)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Comments', to='CaseALK.case')),
            ],
            options={
                'verbose_name_plural': 'ALK Comments',
                'db_table': 'ALK Comment',
                'ordering': ['date_updated'],
            },
        ),
    ]
