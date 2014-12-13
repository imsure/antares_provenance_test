# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('AlertID', models.IntegerField(primary_key=True, serialize=False)),
                ('TakenAt', models.DateTimeField(verbose_name='Time the alert was taken')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AlertReplica',
            fields=[
                ('ReplicaID', models.IntegerField(primary_key=True, serialize=False)),
                ('ReplicaNumber', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('ChannelID', models.IntegerField()),
                ('ChannelProbability', models.FloatField()),
                ('AlertID', models.ForeignKey(to='protracker.Alert')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AstroObject',
            fields=[
                ('AstroObjectID', models.IntegerField(primary_key=True, serialize=False)),
                ('Catalog', models.CharField(max_length=500)),
                ('IDinCatalog', models.IntegerField()),
                ('IsPointSource', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('AttrName', models.CharField(primary_key=True, max_length=100, serialize=False)),
                ('IsScaled', models.BooleanField(default=False)),
                ('DataType', models.CharField(max_length=500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('AttributeValueID', models.IntegerField(primary_key=True, serialize=False)),
                ('ContainerID', models.IntegerField()),
                ('ContainerType', models.CharField(max_length=1, choices=[('A', 'AstroObject Table'), ('C', 'Combo Table'), ('I', 'Image Table'), ('E', 'Alert Table'), ('L', 'LocusAggregatedAlert Table'), ('M', 'ImageSection Table'), ('R', 'AlertReplica Table'), ('S', 'Source Table')])),
                ('ComputedAt', models.DateTimeField(verbose_name='Time the value was computed')),
                ('Value', models.CharField(max_length=500)),
                ('Annotation', models.CharField(max_length=500)),
                ('Confidence', models.FloatField()),
                ('AttrName', models.ForeignKey(to='protracker.Attribute')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DerivedAttribute',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('HashName', models.CharField(max_length=40)),
                ('FunctionName', models.CharField(max_length=50)),
                ('FileName', models.CharField(max_length=50)),
                ('PackageName', models.CharField(max_length=50)),
                ('AstronomerName', models.CharField(max_length=50)),
                ('AttrName', models.ForeignKey(to='protracker.Attribute')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('ImageID', models.IntegerField(primary_key=True, serialize=False)),
                ('TakenAt', models.DateTimeField(verbose_name='Time the image was taken')),
                ('TeloscopeName', models.CharField(max_length=100)),
                ('FilterPassband', models.CharField(max_length=500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Locus',
            fields=[
                ('LocusID', models.IntegerField(primary_key=True, serialize=False)),
                ('Coordinate', models.CharField(max_length=500)),
                ('Uncertainty', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LocusAggregatedAlert',
            fields=[
                ('LAAID', models.IntegerField(primary_key=True, serialize=False)),
                ('LocusID', models.ForeignKey(to='protracker.Locus')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReplicaAssociatedWith',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('AssociationProbability', models.FloatField()),
                ('AstroObjectID', models.ForeignKey(to='protracker.AstroObject')),
                ('ReplicaID', models.ForeignKey(to='protracker.AlertReplica')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('SourceID', models.IntegerField(primary_key=True, serialize=False)),
                ('Coordinate', models.CharField(max_length=500)),
                ('Brightness', models.FloatField()),
                ('DeltaBrightness', models.FloatField()),
                ('ThumbnailURL', models.URLField()),
                ('ImageID', models.ForeignKey(to='protracker.Image')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='attributevalue',
            unique_together=set([('AttrName', 'ContainerID', 'ContainerType', 'ComputedAt')]),
        ),
        migrations.AddField(
            model_name='astroobject',
            name='LocusID',
            field=models.ForeignKey(to='protracker.Locus'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alertreplica',
            name='LocusID',
            field=models.ForeignKey(to='protracker.Locus'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alert',
            name='LAAID',
            field=models.ForeignKey(to='protracker.LocusAggregatedAlert'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alert',
            name='LocusID',
            field=models.ForeignKey(to='protracker.Locus'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alert',
            name='SourceID',
            field=models.ForeignKey(to='protracker.Source'),
            preserve_default=True,
        ),
    ]
