# Generated by Django 4.0.4 on 2022-04-16 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RiktamGroupChatApp', '0005_alter_rgcagroups_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='rgcagroupmembers',
            name='added_by',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
