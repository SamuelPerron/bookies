# Generated by Django 4.1.1 on 2022-09-25 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('odds', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name_plural': 'Cities'},
        ),
        migrations.AlterModelOptions(
            name='match',
            options={'verbose_name_plural': 'Matches'},
        ),
        migrations.AlterModelOptions(
            name='odds',
            options={'verbose_name_plural': 'Odds'},
        ),
        migrations.AlterField(
            model_name='odds',
            name='away_odds',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='odds',
            name='home_odds',
            field=models.FloatField(blank=True),
        ),
    ]