# Generated by Django 3.2.2 on 2021-06-21 09:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CaseALK', '0018_alter_approval_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approval',
            name='case',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approvals', to='CaseALK.case'),
        ),
    ]