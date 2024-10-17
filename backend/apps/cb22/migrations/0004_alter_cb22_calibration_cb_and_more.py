# Generated by Django 5.1.1 on 2024-10-16 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cb22', '0003_cb22_calibration_feb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cb22_calibration',
            name='CB',
            field=models.IntegerField(default=22),
        ),
        migrations.AlterField(
            model_name='cb22_calibration',
            name='mode',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='cb22_calibration',
            name='ROB',
            field=models.IntegerField(default=15),
        ),
        migrations.AlterField(
            model_name='cb22_calibration',
            name='WALL',
            field=models.IntegerField(default=1),
        ),
        migrations.DeleteModel(
            name='CB_list',
        ),
        migrations.DeleteModel(
            name='Mode_list',
        ),
        migrations.DeleteModel(
            name='ROB_list',
        ),
        migrations.DeleteModel(
            name='WALL_list',
        ),
    ]