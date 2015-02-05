# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('rango', '0004_auto_20150125_1623'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='veiws',
            new_name='views',
        ),
    ]
