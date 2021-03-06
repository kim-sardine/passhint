# Generated by Django 2.0.1 on 2018-02-24 07:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import passhint.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('passhint', '0016_auto_20180224_1610'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportRuleSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('len_min', models.SmallIntegerField(blank=True, null=True)),
                ('len_max', models.SmallIntegerField(blank=True, null=True)),
                ('exc_special', models.BooleanField(default=False)),
                ('exc_space', models.BooleanField(default=False)),
                ('exc_same', models.BooleanField(default=False)),
                ('exc_series', models.BooleanField(default=False)),
                ('exc_id', models.BooleanField(default=False)),
                ('exc_common', models.BooleanField(default=False)),
                ('inc_special', models.BooleanField(default=False)),
                ('inc_lower', models.BooleanField(default=False)),
                ('inc_upper', models.BooleanField(default=False)),
                ('inc_number', models.BooleanField(default=False)),
                ('inc_letter', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('waiting', 'waiting'), ('approved', 'approved'), ('rejected', 'rejected'), ('late', 'late')], default='waiting', max_length=10)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_rule_sets', to='passhint.Site')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ReportSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=60)),
                ('status', models.CharField(choices=[('waiting', 'waiting'), ('approved', 'approved'), ('rejected', 'rejected'), ('late', 'late')], default='waiting', max_length=10)),
                ('main_url', models.CharField(max_length=100, validators=[passhint.models.url_validator])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
