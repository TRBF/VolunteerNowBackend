# Generated by Django 5.1.1 on 2025-02-03 21:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0010_alter_callout_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callout',
            name='opportunity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='volunteering.opportunity'),
        ),
    ]
