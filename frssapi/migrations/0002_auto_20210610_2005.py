# Generated by Django 3.2.4 on 2021-06-10 20:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('frssapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('select_answer', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='questions',
            name='text',
        ),
        migrations.AddField(
            model_name='questions',
            name='explanation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='ScoreSheet',
        ),
        migrations.AddField(
            model_name='answers',
            name='question_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frssapi.questions'),
        ),
        migrations.AddField(
            model_name='answers',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]