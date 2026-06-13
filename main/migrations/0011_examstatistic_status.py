# Generated migration for ExamStatistic status field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_examsubmission_fields_and_statistics'),
    ]

    operations = [
        migrations.AddField(
            model_name='examstatistic',
            name='status',
            field=models.CharField(
                choices=[
                    ('not_started', 'Boshlash'),
                    ('in_progress', 'Davom etyapti'),
                    ('completed', 'Yechilgan'),
                ],
                default='not_started',
                max_length=20
            ),
        ),
        migrations.AddIndex(
            model_name='examstatistic',
            index=models.Index(fields=['user', 'status'], name='main_examst_user_id_status_idx'),
        ),
        migrations.AddIndex(
            model_name='examstatistic',
            index=models.Index(fields=['exam', 'is_completed'], name='main_examst_exam_id_is_compl_idx'),
        ),
    ]
