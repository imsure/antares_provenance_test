# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('protracker', '0003_alert_decision'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='TeloscopeName',
            new_name='TelescopeName',
        ),
        migrations.AlterField(
            model_name='alert',
            name='Decision',
            field=models.CharField(choices=[('NA', 'Not Applicable'), ('T', 'Throttled Alert'), ('D', 'Diverted immediately'), ('S1', 'Stage-I Alert'), ('S2', 'Stage-II Alert'), ('R', 'Rarest of the rare Alert')], default='NA', max_length=50),
            preserve_default=True,
        ),
    ]
