# Generated by Django 4.1.5 on 2023-04-13 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myAdmin', '0009_remove_class_section_id_class_section_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='section_id',
        ),
        migrations.CreateModel(
            name='ClassSection',
            fields=[
                ('adminbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='myAdmin.adminbase')),
                ('class_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myAdmin.class')),
                ('section_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myAdmin.section')),
            ],
            options={
                'db_table': 'class_section',
            },
            bases=('myAdmin.adminbase',),
        ),
    ]
