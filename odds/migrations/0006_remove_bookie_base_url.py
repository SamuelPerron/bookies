# Generated by Django 4.1.1 on 2022-09-25 23:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('odds', '0005_remove_match_away_team_remove_match_home_team_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookie',
            name='base_url',
        ),
    ]