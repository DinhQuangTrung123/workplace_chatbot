# Generated by Django 3.1.2 on 2021-11-27 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminsite', '0003_auto_20211126_2218'),
    ]

    operations = [
        migrations.RenameField(
            model_name='campaign',
            old_name='Campaign_Sate',
            new_name='Campaign_Status',
        ),
    ]