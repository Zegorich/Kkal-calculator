# Generated by Django 5.0.4 on 2024-05-21 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0003_alter_user_current_weight_alter_user_desired_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.CharField(default='Male', max_length=50),
            preserve_default=False,
        ),
    ]