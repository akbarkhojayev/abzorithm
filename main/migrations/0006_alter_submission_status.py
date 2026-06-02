# Generated migration

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_category_problem_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='status',
            field=models.CharField(
                choices=[
                    ('Accepted', 'Accepted'),
                    ('Wrong Answer', 'Wrong Answer'),
                    ('Runtime Error', 'Runtime Error'),
                    ('Time Limit Exceeded', 'Time Limit Exceeded'),
                ],
                default='Wrong Answer',
                max_length=20
            ),
        ),
    ]
