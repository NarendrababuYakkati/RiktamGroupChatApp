# Generated by Django 4.0.4 on 2022-04-15 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RiktamGroupChatApp', '0003_rgcagroupmembers_rename_rgca_groups_rgcagroups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rgcagroups',
            name='is_deleted',
            field=models.IntegerField(default=0),
        ),
    ]
