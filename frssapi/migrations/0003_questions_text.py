# Generated by Django 3.2.4 on 2021-06-10 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frssapi', '0002_auto_20210610_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='text',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
