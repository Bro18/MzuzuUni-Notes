# Generated by Django 5.2.3 on 2025-07-22 09:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes_app', '0003_semester_studentprofile_is_approved_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['code']},
        ),
        migrations.AlterModelOptions(
            name='note',
            options={'ordering': ['-upload_date']},
        ),
        migrations.AlterModelOptions(
            name='semester',
            options={'ordering': ['-start_date']},
        ),
        migrations.AlterModelOptions(
            name='studentprofile',
            options={'ordering': ['user__last_name', 'user__first_name']},
        ),
        migrations.AddField(
            model_name='course',
            name='credits',
            field=models.PositiveIntegerField(default=3),
        ),
        migrations.AddField(
            model_name='note',
            name='uploaded_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uploaded_notes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='course',
            name='code',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='programs',
            field=models.ManyToManyField(related_name='courses', to='notes_app.program'),
        ),
        migrations.AlterField(
            model_name='course',
            name='semester',
            field=models.IntegerField(choices=[(1, 'Semester 1'), (2, 'Semester 2'), (3, 'Semester 3'), (4, 'Semester 4'), (5, 'Semester 5'), (6, 'Semester 6')], default=1),
        ),
        migrations.AlterField(
            model_name='course',
            name='year',
            field=models.IntegerField(choices=[(1, 'Year 1'), (2, 'Year 2'), (3, 'Year 3')], default=1),
        ),
        migrations.AlterField(
            model_name='note',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='notes_app.course'),
        ),
        migrations.AlterField(
            model_name='program',
            name='code',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='semester',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='current_semester',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='notes_app.semester'),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='program',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='notes_app.program'),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='semester',
            field=models.IntegerField(choices=[(1, 'Semester 1'), (2, 'Semester 2'), (3, 'Semester 3'), (4, 'Semester 4'), (5, 'Semester 5'), (6, 'Semester 6')], default=1),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='year_of_study',
            field=models.IntegerField(choices=[(1, 'Year 1'), (2, 'Year 2'), (3, 'Year 3')], default=1),
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together={('code', 'name')},
        ),
        migrations.AddConstraint(
            model_name='semester',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_semester_name'),
        ),
    ]
