# Generated by Django 2.0.1 on 2018-02-14 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passhint', '0009_auto_20180214_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='tag',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
