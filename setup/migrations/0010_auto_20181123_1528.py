# Generated by Django 2.1.3 on 2018-11-23 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0009_auto_20181123_1519'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='etapaprocesso',
            options={'verbose_name': 'Etapa do Processo', 'verbose_name_plural': 'Etapas do Processo'},
        ),
        migrations.AlterUniqueTogether(
            name='etapaprocesso',
            unique_together={('op', 'etapa')},
        ),
    ]