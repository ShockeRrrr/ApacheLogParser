# Generated by Django 3.2 on 2021-04-11 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ip', models.CharField(max_length=50)),
            ],
        ),
    ]