# Generated by Django 5.0 on 2023-12-08 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_rename_post_title_comment_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post',
            new_name='post_title',
        ),
    ]
