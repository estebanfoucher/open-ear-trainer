from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="lesson",
            name="theory_title",
            field=models.CharField(blank=True, default="", max_length=200),
        ),
        migrations.AddField(
            model_name="lesson",
            name="theory_markdown",
            field=models.TextField(blank=True, default=""),
        ),
    ]
