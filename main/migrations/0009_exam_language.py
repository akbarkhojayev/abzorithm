# Generated migration for adding language field to Exam

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_exam_examsubmission_examassignment_examquestion'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='language',
            field=models.CharField(
                choices=[('python', 'Python'), ('javascript', 'JavaScript'), ('dart', 'Dart')],
                default='python',
                max_length=20
            ),
        ),
    ]
