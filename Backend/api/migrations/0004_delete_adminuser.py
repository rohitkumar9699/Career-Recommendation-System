from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_student_username'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AdminUser',
        ),
    ]