# Generated by Django 2.1.3 on 2018-11-26 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0011_auto_20181123_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setup',
            name='processo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='setup.EtapaProcesso', verbose_name='Etapa do Processo'),
        ),
    ]
