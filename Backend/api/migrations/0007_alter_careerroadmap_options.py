from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0006_expand_careerroadmap'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='careerroadmap',
            options={'ordering': ['-score', 'career']},
        ),
    ]
