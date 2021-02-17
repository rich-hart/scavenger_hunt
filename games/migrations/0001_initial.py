# Generated by Django 3.1.6 on 2021-02-17 20:28

from django.db import migrations, models
import django.db.models.deletion
import games.models
import hunt.storage_backends


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('index', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['index', 'id'],
                'permissions': [('access_challenge', 'Can access the challenge')],
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('solution_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='games.solution')),
                ('text', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=('games.solution',),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('problem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='games.problem')),
                ('text', models.TextField()),
                ('video', models.FileField(blank=True, default=None, null=True, storage=hunt.storage_backends.MediaStorage(), upload_to='')),
                ('picture', models.FileField(blank=True, default=None, null=True, storage=hunt.storage_backends.MediaStorage(), upload_to='')),
            ],
            options={
                'abstract': False,
            },
            bases=('games.problem',),
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(choices=[(0, games.models.Reward.Type['general']), (1, games.models.Reward.Type['clue']), (2, games.models.Reward.Type['praise']), (3, games.models.Reward.Type['points']), (4, games.models.Reward.Type['key']), (5, games.models.Reward.Type['powers']), (6, games.models.Reward.Type['promotion']), (7, games.models.Reward.Type['completion']), (8, games.models.Reward.Type['media'])], default='general', max_length=127)),
                ('description', models.TextField()),
                ('unique', models.BooleanField(default=True)),
                ('rate', models.FloatField(default=1.0)),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='games.challenge')),
            ],
            options={
                'ordering': ['-created'],
                'permissions': [('access_reward', 'Can access the reward')],
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Penalty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[(0, games.models.Penalty.Type['yellow']), (1, games.models.Penalty.Type['red']), (2, games.models.Penalty.Type['general'])], default='general', max_length=127)),
                ('description', models.TextField()),
                ('duration', models.IntegerField(default=300)),
                ('game', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='games.game')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='games.player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(to='games.Player'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='game',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='challenges', to='games.game'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='problem',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='games.problem'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='solution',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='games.solution'),
        ),
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('verified', models.BooleanField(blank=True, default=None, null=True)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='games.player')),
                ('reward', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='games.reward')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='games.challenge')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.player')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
