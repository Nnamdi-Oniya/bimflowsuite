from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("parametric_generator", "0008_remove_site_project_type_alter_site_type_metadata"),
    ]

    operations = [
        migrations.CreateModel(
            name="Material",
            fields=[
                ("id", models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("code", models.CharField(max_length=100, blank=True, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("properties", models.JSONField(default=dict, blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("facility", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="materials", to="parametric_generator.facility")),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.AddField(
            model_name="element",
            name="material",
            field=models.ForeignKey(blank=True, null=True, on_delete=models.deletion.SET_NULL, related_name="elements", to="parametric_generator.material"),
        ),
        migrations.AddField(
            model_name="element",
            name="geometry",
            field=models.JSONField(default=dict, blank=True),
        ),
        migrations.AddField(
            model_name="element",
            name="position",
            field=models.JSONField(default=dict, blank=True),
        ),
    ]
