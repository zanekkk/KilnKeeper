# Generated by Django 3.0.1 on 2022-09-15 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kilnkeeperconsole', '0007_auto_20220906_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firing',
            name='History',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='kilnkeeperconsole.History'),
        ),
    ]
