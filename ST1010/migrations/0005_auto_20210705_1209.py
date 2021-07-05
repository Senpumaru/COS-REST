# Generated by Django 3.2.4 on 2021-07-05 09:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ST1010', '0004_auto_20210705_1201'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permission',
            name='is_registrator',
        ),
        migrations.AddField(
            model_name='permission',
            name='is_registrar',
            field=models.BooleanField(default=False, help_text="ST1010 permissions for Registrar's access.", verbose_name='Registrar Status'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='is_clinician',
            field=models.BooleanField(default=False, help_text="ST1010 permissions for Clinician's access.", verbose_name='Clinician Status'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='is_consultant',
            field=models.BooleanField(default=False, help_text="ST1010 permissions for Consultant's access.", verbose_name='Consultant Status'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='is_guest',
            field=models.BooleanField(default=True, help_text="ST1010 permissions for Guests's access.", verbose_name='Guest Status'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='is_pathologist',
            field=models.BooleanField(default=False, help_text="ST1010 elevated permissions for Pathologist's access.", verbose_name='Pathologist Status'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ST1010_Permission', to=settings.AUTH_USER_MODEL),
        ),
    ]
