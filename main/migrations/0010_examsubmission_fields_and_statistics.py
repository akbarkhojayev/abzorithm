# Generated migration for ExamStatistic model and ExamSubmission updates

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_exam_language'),
    ]

    operations = [
        # Update ExamSubmission model
        migrations.AddField(
            model_name='examsubmission',
            name='is_exam_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='examsubmission',
            name='completed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='examsubmission',
            name='status',
            field=models.CharField(
                choices=[
                    ('Accepted', 'Accepted'),
                    ('Wrong Answer', 'Wrong Answer'),
                    ('Runtime Error', 'Runtime Error'),
                    ('Time Limit Exceeded', 'Time Limit Exceeded')
                ],
                default='Wrong Answer',
                max_length=20
            ),
        ),
        # Create ExamStatistic model
        migrations.CreateModel(
            name='ExamStatistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_problems', models.IntegerField(default=0)),
                ('solved_problems', models.IntegerField(default=0)),
                ('attempted_problems', models.IntegerField(default=0)),
                ('total_submissions', models.IntegerField(default=0)),
                ('correct_submissions', models.IntegerField(default=0)),
                ('time_spent_minutes', models.IntegerField(default=0)),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('score', models.IntegerField(default=0)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statistics', to='main.exam')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exam_statistics', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Exam Statistics',
                'unique_together': {('user', 'exam')},
            },
        ),
    ]
