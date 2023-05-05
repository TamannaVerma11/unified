# Generated by Django 4.1.5 on 2023-04-26 18:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myAdmin', '0002_rename_medium_id_class_medium_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categories',
            old_name='created_by',
            new_name='creator',
        ),
        migrations.RenameField(
            model_name='class',
            old_name='created_by',
            new_name='creator',
        ),
        migrations.RenameField(
            model_name='designation',
            old_name='created_by',
            new_name='creator',
        ),
        migrations.RenameField(
            model_name='medium',
            old_name='created_by',
            new_name='creator',
        ),
        migrations.RenameField(
            model_name='section',
            old_name='created_by',
            new_name='creator',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='created_by',
            new_name='creator',
        ),
        migrations.RenameField(
            model_name='teacher',
            old_name='created_by',
            new_name='creator',
        ),
        migrations.RemoveField(
            model_name='department',
            name='created_by',
        ),
        migrations.AddField(
            model_name='department',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
