from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("assignments", "0012_teachertask_show_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="teachertask",
            name="department",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tasks",
                to="assignments.department",
            ),
        ),
        migrations.AlterField(
            model_name="teachertask",
            name="level",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tasks",
                to="assignments.level",
            ),
        ),
        migrations.AlterField(
            model_name="teachertask",
            name="semester",
            field=models.PositiveIntegerField(),
        ),
    ]
