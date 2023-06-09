# Generated by Django 4.1.7 on 2023-03-11 21:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_adminprofile_id_alter_user_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='referrals_left',
            field=models.IntegerField(blank=True, default=5, null=True),
        ),
        migrations.AddField(
            model_name='userdata',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
