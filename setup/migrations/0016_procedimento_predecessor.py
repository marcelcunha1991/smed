# Generated by Django 2.1.3 on 2018-11-27 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0015_auto_20181126_0924'),
    ]

    operations = [
        migrations.AddField(
            model_name='procedimento',
            name='predecessor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='setup.Procedimento'),
        ),
    ]