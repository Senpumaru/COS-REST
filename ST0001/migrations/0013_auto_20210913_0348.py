# Generated by Django 3.2.5 on 2021-09-13 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ST0001', '0012_auto_20210912_0657'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='count',
            field=models.IntegerField(blank=True, null=True, verbose_name='Block Count'),
        ),
        migrations.AddField(
            model_name='block',
            name='startCode',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Block Code Start'),
        ),
        migrations.AlterField(
            model_name='block',
            name='block_group',
            field=models.ForeignKey(max_length=20, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='BlockGroup_Block', to='ST0001.blockgroup', verbose_name='Block Group'),
        ),
    ]
