# Generated by Django 3.0.1 on 2022-09-04 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kilnkeeperconsole', '0005_actualkilnstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='actualkilnstatus',
            name='schedule_id',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
