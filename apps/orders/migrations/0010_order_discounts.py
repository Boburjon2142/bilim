from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0009_order_crm_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="subtotal_before_discount",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name="Chegirmasiz summa"),
        ),
        migrations.AddField(
            model_name="order",
            name="discount_percent",
            field=models.PositiveIntegerField(default=0, verbose_name="Chegirma (%)"),
        ),
        migrations.AddField(
            model_name="order",
            name="discount_amount",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name="Chegirma summasi"),
        ),
    ]
