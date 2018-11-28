# Generated by Django 2.1.3 on 2018-11-26 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0013_auto_20181126_0903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='procedimento',
            name='status',
            field=models.IntegerField(blank=True, choices=[(0, 'Pendente'), (1, 'Realizando'), (2, 'Realizado com sucesso'), (3, 'Realizado fora do tempo'), (4, 'Realizado com justificativa')], default=0, null=True),
        ),
    ]
