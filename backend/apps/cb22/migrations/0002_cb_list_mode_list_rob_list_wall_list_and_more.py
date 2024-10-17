# Generated by Django 5.1.1 on 2024-10-16 09:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cb22', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CB_list',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('CB', models.IntegerField()),
            ],
            options={
                'db_table': 'CB_list',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Mode_list',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('mode', models.IntegerField()),
            ],
            options={
                'db_table': 'mode_list',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ROB_list',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('ROB', models.IntegerField()),
            ],
            options={
                'db_table': 'ROB_list',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='WALL_list',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('WALL', models.IntegerField()),
            ],
            options={
                'db_table': 'WALL_list',
                'ordering': ['id'],
            },
        ),
        migrations.AlterModelOptions(
            name='cb22_calibration',
            options={'ordering': ['id']},
        ),
        migrations.RemoveField(
            model_name='cb22_calibration',
            name='FEB',
        ),
        migrations.AlterField(
            model_name='cb22_calibration',
            name='CB',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cb22.cb_list'),
        ),
        migrations.AlterField(
            model_name='cb22_calibration',
            name='mode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cb22.mode_list'),
        ),
        migrations.AlterField(
            model_name='cb22_calibration',
            name='ROB',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cb22.rob_list'),
        ),
        migrations.AlterField(
            model_name='cb22_calibration',
            name='WALL',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cb22.wall_list'),
        ),
    ]