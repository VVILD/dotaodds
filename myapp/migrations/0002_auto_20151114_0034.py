# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='links',
            name='linktype',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'd2l', b'dota2lounge'), (b'vpd', b'vpgame dota'), (b'vpp', b'vpgame p coins'), (b'd2byd', b'dota 2 bestyolo dota'), (b'd2byc', b'dota 2 bestyolo csgo'), (b'd2t', b'dota 2 top'), (b'nxt', b'nxtgame')]),
            preserve_default=True,
        ),
    ]
