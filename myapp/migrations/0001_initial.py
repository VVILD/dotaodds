# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('link', models.CharField(max_length=500)),
                ('team1odd', models.FloatField(default=1.0)),
                ('team2odd', models.FloatField(default=1.0)),
                ('time_left', models.CharField(max_length=500, null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('linktype', models.CharField(blank=True, max_length=10, null=True, choices=[(b'd2l', b'dota2lounge'), (b'vpd', b'vpgame dota'), (b'vpp', b'vpgame p coins'), (b'd2byd', b'dota 2 bestyolo dota'), (b'd2byc', b'dota 2 bestyolo csgo')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='links',
            name='match',
            field=models.ForeignKey(to='myapp.Match'),
            preserve_default=True,
        ),
    ]
