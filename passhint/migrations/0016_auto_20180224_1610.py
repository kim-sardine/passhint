# Generated by Django 2.0.1 on 2018-02-24 07:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('passhint', '0015_auto_20180220_1433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportruleset',
            name='site',
        ),
        migrations.RemoveField(
            model_name='reportruleset',
            name='user',
        ),
        migrations.RemoveField(
            model_name='reportsite',
            name='user',
        ),
        migrations.DeleteModel(
            name='ReportRuleSet',
        ),
        migrations.DeleteModel(
            name='ReportSite',
        ),
    ]