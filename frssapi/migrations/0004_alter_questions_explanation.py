# Generated by Django 3.2.4 on 2021-06-18 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frssapi', '0003_auto_20210617_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='explanation',
            field=models.TextField(null=True),
        ),
    ]
