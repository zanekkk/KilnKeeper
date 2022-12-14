# Generated by Django 3.0.1 on 2022-09-06 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kilnkeeperconsole', '0006_actualkilnstatus_schedule_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='kilnsettings',
            name='Kiln_power',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='kilnsettings',
            name='kWh_cost',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='kilnsettings',
            name='Max_kiln_temperature',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
