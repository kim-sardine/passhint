# Generated by Django 2.0.1 on 2018-02-14 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passhint', '0007_auto_20180203_2325'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='status',
            field=models.CharField(choices=[('service', 'service'), ('waiting', 'waiting'), ('rejected', 'rejected')], default='waiting', max_length=10),
        ),
    ]
