from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("parametric_generator", "0003_project_project_image_site_site_image"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Asset",
            new_name="Element",
        ),
    ]
