# Generated by Django 4.1.7 on 2023-02-22 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coordinator', '0004_scan_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='scan',
            name='date',
            field=models.DateField(null=True),
        ),
    ]