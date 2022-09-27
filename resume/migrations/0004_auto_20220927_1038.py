# Generated by Django 3.2.11 on 2022-09-27 10:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('resume', '0003_auto_20220927_0904'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='exp',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='resume',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Image', to=settings.AUTH_USER_MODEL),
        ),
    ]