# Generated by Django 4.1.1 on 2022-09-23 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bookie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('base_url', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=4)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_set', to='odds.city')),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_set', to='odds.league')),
            ],
        ),
        migrations.CreateModel(
            name='Odds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('away_odds', models.FloatField()),
                ('home_odds', models.FloatField()),
                ('bookie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='odds_set', to='odds.bookie')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='odds_set', to='odds.match')),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='away_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_match_set', to='odds.team'),
        ),
        migrations.AddField(
            model_name='match',
            name='home_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_match_set', to='odds.team'),
        ),
        migrations.AddField(
            model_name='match',
            name='league',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_set', to='odds.league'),
        ),
    ]
