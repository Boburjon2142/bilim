from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("crm", "0001_initial"),
        ("orders", "0008_deliverysettings_shop_location_link"),
    ]

    operations = [
        migrations.AddField(
            model_name="inventorylog",
            name="related_order",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.SET_NULL,
                related_name="inventory_logs",
                to="orders.order",
            ),
        ),
    ]
