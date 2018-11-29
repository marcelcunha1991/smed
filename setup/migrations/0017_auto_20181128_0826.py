# Generated by Django 2.1.3 on 2018-11-28 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0016_procedimento_predecessor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='procedimento',
            name='status',
            field=models.IntegerField(blank=True, choices=[(1, 'Pendente'), (2, 'Realizando'), (3, 'Realizado com sucesso'), (4, 'Realizado fora do tempo'), (5, 'Realizado com justificativa')], default=0, null=True),
        ),
    ]