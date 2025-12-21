from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0008_merge_20251204_1149"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="barcode",
            field=models.CharField(blank=True, max_length=64, null=True, unique=True, verbose_name="Shtrix-kod"),
        ),
        migrations.AddField(
            model_name="book",
            name="stock_quantity",
            field=models.IntegerField(default=0, verbose_name="Ombor"),
        ),
    ]
