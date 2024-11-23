# Generated by Django 5.1.3 on 2024-11-23 08:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_organization_name_sub_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sub_organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='myapp.sub_organization'),
        ),
    ]
