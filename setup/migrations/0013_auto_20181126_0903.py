# Generated by Django 2.1.3 on 2018-11-26 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0012_auto_20181126_0853'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='setup',
            unique_together={('processo', 'tipo')},
        ),
    ]
