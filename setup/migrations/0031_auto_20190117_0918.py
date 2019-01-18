# Generated by Django 2.1.3 on 2019-01-17 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0030_auto_20190114_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='procedimento',
            name='hora_fim',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='procedimento',
            name='hora_inicio',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='procedimento',
            name='tempo_realizado2',
            field=models.DurationField(blank=True, null=True),
        ),
    ]