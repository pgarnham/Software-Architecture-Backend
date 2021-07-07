# Generated by Django 3.1 on 2020-11-04 02:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20201012_1441'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True, max_length=30)),
                ('room', models.CharField(max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='roommessage',
            name='room',
        ),
        migrations.RemoveField(
            model_name='roommessage',
            name='user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='password',
        ),
        migrations.DeleteModel(
            name='Room',
        ),
        migrations.DeleteModel(
            name='RoomMessage',
        ),
        migrations.AddField(
            model_name='message',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.user'),
        ),
    ]
