from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("crm", "0002_inventorylog_order_link"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="discount_percent",
            field=models.PositiveIntegerField(default=0, verbose_name="Chegirma (%)"),
        ),
    ]
