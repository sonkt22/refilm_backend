# Generated by Django 3.0.5 on 2020-06-21 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_remove_userlikepost_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercommentpost',
            name='content',
            field=models.CharField(blank=True, max_length=1200, null=True),
        ),
    ]
