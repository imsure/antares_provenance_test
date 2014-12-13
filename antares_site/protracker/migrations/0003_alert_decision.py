# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('protracker', '0002_remove_alert_laaid'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='Decision',
            field=models.CharField(choices=[('NA', 'Not Applicable'), ('T', 'Throttled Alert'), ('S1', 'Stage-I Alert'), ('S2', 'Stage-II Alert'), ('R', 'Rarest of the rare Alert')], default='NA', max_length=50),
            preserve_default=True,
        ),
    ]
