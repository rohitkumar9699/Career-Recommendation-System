from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0005_careerroadmap'),
    ]

    operations = [
        migrations.RenameField(
            model_name='careerroadmap',
            old_name='recommendations',
            new_name='degree_course',
        ),
        migrations.RemoveField(
            model_name='careerroadmap',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='careerroadmap',
            name='career',
            field=models.CharField(default='Unknown', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='careerroadmap',
            name='score',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='careerroadmap',
            name='what_you_do',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='careerroadmap',
            name='skills',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='careerroadmap',
            name='what_to_explore',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='careerroadmap',
            name='student',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='career_roadmaps',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddConstraint(
            model_name='careerroadmap',
            constraint=models.UniqueConstraint(
                fields=('student', 'career'),
                name='unique_student_career_roadmap',
            ),
        ),
    ]
