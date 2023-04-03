# Generated by Django 4.1.7 on 2023-04-03 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coordinator', '0005_scan_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scan',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='scan',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='scan',
            name='schedule',
            field=models.CharField(choices=[('Weekly', 'Weekly'), ('Monthly', 'Monthly'), ('Quarterly', 'Quarterly'), ('Yearly', 'Yearly')], default='Weekly', max_length=255),
        ),
    ]
